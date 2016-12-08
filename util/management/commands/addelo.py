from time import clock

from bulk_update.helper import bulk_update
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F
from trueskill import Rating, rate

from FRS.settings import SOFT_RESET_SCALE, DEFAULT_SIGMA, DEFAULT_MU, SUPPORTED_YEARS
from TBAW.models import Event, RankingModel, Team, Alliance, Match
from leaderboard.models import TeamLeaderboard

matches_added = 0


def handle_match_elo(match: Match) -> None:
    global matches_added

    drawn = False
    if match.winner is None:
        drawn = True
        alliance_winner = match.alliances.all()[0]
        team_winners = alliance_winner.teams.all()
    else:
        alliance_winner = match.winner
        team_winners = alliance_winner.teams.all()

    alliance_loser_list = match.alliances.exclude(id=match.winner_id).all()
    alliance_loser = [x for x in alliance_loser_list][0]
    team_losers = alliance_loser.teams.all()

    # alliance_winner_ts = Rating(alliance_winner.elo_mu, alliance_winner.elo_sigma)
    # alliance_loser_ts = Rating(alliance_loser.elo_mu, alliance_loser.elo_sigma)
    # alliance_results = rate_1vs1(alliance_winner_ts, alliance_loser_ts, drawn=drawn)
    #
    # alliance_winner.elo_mu = alliance_results[0].mu
    # alliance_winner.elo_sigma = alliance_results[0].sigma
    # alliance_loser.elo_mu = alliance_results[1].mu
    # alliance_loser.elo_sigma = alliance_results[1].sigma
    # alliance_winner.save(update_fields=['elo_mu', 'elo_sigma'])
    # alliance_loser.save(update_fields=['elo_mu', 'elo_sigma'])

    team_winner_ts_pairs = [(t, Rating(t.elo_mu, t.elo_sigma)) for t in team_winners]
    team_loser_ts_pairs = [(t, Rating(t.elo_mu, t.elo_sigma)) for t in team_losers]

    if drawn:
        team_results = rate([[x[1] for x in team_winner_ts_pairs], [x[1] for x in team_loser_ts_pairs]], ranks=[0, 0])
    else:
        team_results = rate([[x[1] for x in team_winner_ts_pairs], [x[1] for x in team_loser_ts_pairs]])

    with transaction.atomic():
        for winner_result, winner_team, loser_result, loser_team in zip(team_results[0], team_winners, team_results[1],
                                                                        team_losers):
            winner_team.elo_mu = winner_result.mu
            winner_team.elo_sigma = winner_result.sigma
            loser_team.elo_mu = loser_result.mu
            loser_team.elo_sigma = loser_result.sigma

            winner_team.save(update_fields=['elo_mu', 'elo_sigma'])
            loser_team.save(update_fields=['elo_mu', 'elo_sigma'])

    matches_added += 1
    # print("({1}) Handled {0}".format(match, matches_added))


def add_all_elo(year: int) -> None:
    events = Event.objects.filter(year=year).order_by('end_date')
    for e in events:
        add_event_elo(e)


def add_event_elo(event: Event) -> None:
    print("Adding Elo for event {0}... ".format(event.key), end="", flush=True)

    allianceappearances = event.allianceappearance_set.select_related('alliance').all()
    for appearance in allianceappearances:
        appearance.elo_mu_pre = appearance.alliance.elo_mu
        appearance.elo_sigma_pre = appearance.alliance.elo_sigma

    bulk_update(allianceappearances, update_fields=['elo_mu_pre', 'elo_sigma_pre'])

    rms = event.rankingmodel_set.select_related('team').all()
    with transaction.atomic():
        for rm in rms:
            t = rm.team
            rm.elo_mu_pre = t.elo_mu
            rm.elo_sigma_pre = t.elo_sigma
            rm.save(update_fields=['elo_mu_pre', 'elo_sigma_pre'])

    for match in event.match_set.select_related('winner').prefetch_related('alliances__teams').all():
        handle_match_elo(match)

    for appearance in event.allianceappearance_set.all():
        appearance.elo_mu_post = appearance.alliance.elo_mu
        appearance.elo_sigma_post = appearance.alliance.elo_sigma

    bulk_update(event.allianceappearance_set.all(), update_fields=['elo_mu_post', 'elo_sigma_post'])

    teams = event.teams.all()
    rankings = {rm.team_id: rm for rm in RankingModel.objects.filter(team_id__in=[t.id for t in teams],
                                                                     event_id=event.id)}

    for team in teams:
        ranking = rankings[team.id]
        ranking.elo_mu_post = team.elo_mu
        ranking.elo_sigma_post = team.elo_sigma

    bulk_update(list(rankings.values()), update_fields=['elo_mu_post', 'elo_sigma_post'])
    print("Done!")


def soft_reset(value=SOFT_RESET_SCALE) -> None:
    Team.objects.filter(event__year=SUPPORTED_YEARS[-1]).distinct().exclude(elo_sigma=DEFAULT_SIGMA).update(
        elo_mu=F('elo_mu') - (F('elo_mu') - DEFAULT_MU) * value,
        elo_sigma=F('elo_sigma') - (F('elo_sigma') - DEFAULT_SIGMA) * value
    )
    Alliance.objects.filter(event__year=SUPPORTED_YEARS[-1]).distinct().exclude(elo_sigma=DEFAULT_SIGMA).update(
        elo_mu=F('elo_mu') - (F('elo_mu') - DEFAULT_MU) * value,
        elo_sigma=F('elo_sigma') - (F('elo_sigma') - DEFAULT_SIGMA) * value
    )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--log', action='store_true', dest='log', default=False)
        parser.add_argument('--event', dest='event', default='', type=str)
        parser.add_argument('--year', dest='year', default=0, type=int)

    def handle(self, *args, **options):
        log = options['log']
        year = options['year']
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
                    soft_reset()

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
