from time import clock

from django.core.management.base import BaseCommand
from django.db.models import F, Q
from trueskill import Rating, rate_1vs1, rate

from FRS.settings import DEFAULT_SIGMA, DEFAULT_MU, SUPPORTED_YEARS, ELO_DECAY_ALPHA
from TBAW.models import Event, Team, Alliance, Match, AllianceAppearance
from leaderboard.models import TeamLeaderboard

matches_added = 0
verbose = False

old_print = print

def new_print(*args, **kwargs):
    is_verbose = kwargs.pop("verbose", True)
    if verbose or not is_verbose:
        old_print(*args, **kwargs)

print = new_print

def handle_match_elo(match: Match) -> None:
    global matches_added, verbose

    print("Handling match", match.key)
    match_alliances = match.alliances.all()
    print("\tDetermining Alliance and Team Winners...")
    drawn = False
    if match.winner is None:
        drawn = True
        ally_winner = match_alliances[0]
        team_winners = ally_winner.teams.all()
    else:
        ally_winner = match.winner
        team_winners = ally_winner.teams.all()

    print("\tSelecting losing alliance...")
    ally_loser = next(x for x in match_alliances if x.id != match.winner_id)
    team_losers = ally_loser.teams.all()

    print("\tRunning Alliance TrueSkill calculations...")
    ally_winner_ts = Rating(ally_winner.elo_mu, ally_winner.elo_sigma)
    ally_loser_ts = Rating(ally_loser.elo_mu, ally_loser.elo_sigma)
    (ally_winner_result, ally_loser_result) = rate_1vs1(ally_winner_ts, ally_loser_ts, drawn=drawn)

    ally_winner.elo_mu = ally_winner_result.mu
    ally_winner.elo_sigma = ally_winner_result.sigma
    ally_loser.elo_mu = ally_loser_result.mu
    ally_loser.elo_sigma = ally_loser_result.sigma


    team_winner_ts_pairs = [(t, Rating(t.elo_mu, t.elo_sigma)) for t in team_winners]
    team_loser_ts_pairs = [(t, Rating(t.elo_mu, t.elo_sigma)) for t in team_losers]

    print("\tRunning Team TrueSkill calculations...")
    if drawn:
        team_results = rate([[x[1] for x in team_winner_ts_pairs], [x[1] for x in team_loser_ts_pairs]], ranks=[0, 0])
    else:
        team_results = rate([[x[1] for x in team_winner_ts_pairs], [x[1] for x in team_loser_ts_pairs]])

    print("\tUpdating team mu and sigma...")
    result_and_teams = zip(team_results[0], team_winners, team_results[1], team_losers)
    for winner_result, winner_team, loser_result, loser_team in result_and_teams:
        winner_team.elo_mu = winner_result.mu
        winner_team.elo_sigma = winner_result.sigma
        loser_team.elo_mu = loser_result.mu
        loser_team.elo_sigma = loser_result.sigma

    print("\tSaving...")
    ally_winner.save(update_fields=['elo_mu', 'elo_sigma'])
    ally_loser.save(update_fields=['elo_mu', 'elo_sigma'])
    Team.objects.bulk_update([*team_winners, *team_losers], update_fields=['elo_mu', 'elo_sigma'])
    print("Done!")
    matches_added += 1


def add_all_elo(year: int) -> None:
    events = Event.objects.filter(year=year).order_by('end_date')
    for e in events:
        add_event_elo(e)


def add_event_elo(event: Event) -> None:
    print("Adding Elo for event {0}... ".format(event.key), verbose=False, flush=True)

    print("Setting pre-mu and pre-sigma for AllianceAppearances...")
    allianceappearances = event.allianceappearance_set.select_related('alliance')
    for appearance in allianceappearances.iterator():
        appearance.elo_mu_pre = appearance.alliance.elo_mu
        appearance.elo_sigma_pre = appearance.alliance.elo_sigma

    print("Getting Teams and RMs...")
    teams = event.teams.all()
    rm_map = {rm.team_id: rm for rm in event.rankingmodel_set.filter(event_id=event.id).all()}
    rms = [*rm_map.values()]

    print("Setting pre-mu and pre-sigma for RMs...")
    for rm in rms:
        t = rm.team
        rm.elo_mu_pre = t.elo_mu
        rm.elo_sigma_pre = t.elo_sigma


    print("Handling matches...")
    matches = event.match_set.select_related('winner').prefetch_related('alliances__teams')
    for match in matches.iterator():
        handle_match_elo(match)

    print("Setting post-mu and post-sigma for AllianceAppearances")
    for appearance in allianceappearances.iterator():
        appearance.elo_mu_post = appearance.alliance.elo_mu
        appearance.elo_sigma_post = appearance.alliance.elo_sigma

    AllianceAppearance.objects.bulk_update(allianceappearances, update_fields=['elo_mu_pre', 'elo_sigma_pre', 'elo_mu_post', 'elo_sigma_post'])

    print("Updating post-mu and post-sigma for RankingModels...")
    for team in teams:
        ranking = rm_map[team.id]
        ranking.elo_mu_post = team.elo_mu
        ranking.elo_sigma_post = team.elo_sigma
        ranking.save()

    print("Done!")


def soft_reset(year: int, value: float=ELO_DECAY_ALPHA) -> None:
    print("Doing soft reset for %d ..." % year, verbose=False)

    print("Soft Reset Teams...")
    Team.objects.prefetch_related('event_set').filter(Q(active_years__contains=year) & Q(event__year=year)).distinct().exclude(Q(elo_mu=DEFAULT_MU) & Q(elo_sigma=DEFAULT_SIGMA)).update(
        elo_mu=(1 - value) * F('elo_mu') + value * DEFAULT_MU,
        elo_sigma=(1 - value) * F('elo_sigma') + value * DEFAULT_SIGMA
    )

    print("Soft Reset Alliances...")
    Alliance.objects.prefetch_related('match_set__event').filter(match__event__year=year).distinct().exclude(Q(elo_mu=DEFAULT_MU) & Q(elo_sigma=DEFAULT_SIGMA)).update(
        elo_mu=(1-value)*F('elo_mu') + value*DEFAULT_MU,
        elo_sigma=(1-value)*F('elo_sigma') + value*DEFAULT_SIGMA
    )
    print("Done!")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--log', action='store_true', dest='log', default=False)
        parser.add_argument('--event', dest='event', default='', type=str)
        parser.add_argument('--year', dest='year', default=0, type=int)
        parser.add_argument('--verbose', action='store_true', dest='verbose', default=False)

    def handle(self, *args, **options):
        global verbose
        log = options['log']
        year = options['year']
        verbose = options['verbose']
        if log:
            with open('elo.tsv', 'w', encoding='utf-8') as file:
                elo_leaders = TeamLeaderboard.highest_elo_scaled()
                row_fmt = "%s\t%s\t%s\t%s"
                file.writelines([
                                    (row_fmt % (
                                        rank, str(team).replace("\t", ""), team.elo_scaled, team.elo_sigma)).replace(
                                        '"',
                                        "''")
                                    for rank, team in enumerate(elo_leaders, start=1)
                                    ])
                # Replace double quotes so we can post it to Gist without Github freaking out
                # Replace tab characters because Team 422 has a tab in their name (WHY?!)
                # More teams have commas than tabs in their names so just uses .tsv file
        elif options['event'] == '':
            time_start = clock()
            if year == 0:
                for yr in SUPPORTED_YEARS[:-1]:
                    add_all_elo(yr)
                    soft_reset(yr)

                add_all_elo(SUPPORTED_YEARS[-1])
            else:
                add_all_elo(year)
            time_end = clock()
            print("-------------")
            print("Matches added:\t\t{0}".format(matches_added))
            print("Ran in {0} seconds.".format(round(time_end - time_start, 3)))
            print("-------------")
        else:
            # add_event_elo(Event.objects.get(key=options['event']))
            from cProfile import Profile
            profiler = Profile()
            profiler.runcall(add_event_elo, Event.objects.get(key=options['event']))
            profiler.print_stats(2)
