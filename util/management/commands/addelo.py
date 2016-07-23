from time import clock

from bulk_update.helper import bulk_update
from django.core.management.base import BaseCommand
from django.db.models import F
from trueskill import Rating, rate, rate_1vs1

from FRS.settings import SOFT_RESET_SCALE, DEFAULT_SIGMA, DEFAULT_MU
from TBAW.models import Event, RankingModel, Team, Alliance
from leaderboard.models import TeamLeaderboard

matches_added = 0


def handle_match_elo(match):
    global matches_added

    drawn = False
    if match.winner is None:
        drawn = True
        alliance_winner = match.alliances.all()[0]
        team_winners = alliance_winner.teams.all()
    else:
        alliance_winner = match.winner
        team_winners = alliance_winner.teams.all()

    alliance_loser = [x for x in match.alliances.all() if x != match.winner][0]
    team_losers = alliance_loser.teams.all()

    alliance_winner_ts = Rating(alliance_winner.elo_mu, alliance_winner.elo_sigma)
    alliance_loser_ts = Rating(alliance_loser.elo_mu, alliance_loser.elo_sigma)
    alliance_results = rate_1vs1(alliance_winner_ts, alliance_loser_ts, drawn=drawn)

    alliance_winner.elo_mu = alliance_results[0].mu
    alliance_winner.elo_sigma = alliance_results[0].sigma
    alliance_loser.elo_mu = alliance_results[1].mu
    alliance_loser.elo_sigma = alliance_results[1].sigma
    alliance_winner.save(update_fields=['elo_mu', 'elo_sigma'])
    alliance_loser.save(update_fields=['elo_mu', 'elo_sigma'])

    team_winner_ts_pairs = [(t, Rating(t.elo_mu, t.elo_sigma)) for t in team_winners]
    team_loser_ts_pairs = [(t, Rating(t.elo_mu, t.elo_sigma)) for t in team_losers]

    if drawn:
        team_results = rate([[x[1] for x in team_winner_ts_pairs], [x[1] for x in team_loser_ts_pairs]], ranks=[0, 0])
    else:
        team_results = rate([[x[1] for x in team_winner_ts_pairs], [x[1] for x in team_loser_ts_pairs]])

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


def add_all_elo(year):
    for e in Event.objects.filter(year=year).exclude(event_code='cmp').exclude(event_code='iri').order_by('end_date'):
        add_event_elo(e)

    add_event_elo(Event.objects.get(year=year, event_code='cmp'))
    add_event_elo(Event.objects.get(year=year, event_code='iri'))


def add_event_elo(event):
    print("Adding Elo for event {0}... ".format(event.key), end="", flush=True)

    for appearance in event.allianceappearance_set.all():
        appearance.elo_mu_pre = appearance.alliance.elo_mu
        appearance.elo_sigma_pre = appearance.alliance.elo_sigma

    bulk_update(event.allianceappearance_set.all(), update_fields=['elo_mu_pre', 'elo_sigma_pre'])

    for rm in event.rankingmodel_set.all():
        t = rm.team
        rm.elo_mu_pre = t.elo_mu
        rm.elo_sigma_pre = t.elo_sigma
        rm.save(update_fields=['elo_mu_pre', 'elo_sigma_pre'])

    for match in event.match_set.all():
        handle_match_elo(match)

    for appearance in event.allianceappearance_set.all():
        appearance.elo_mu_post = appearance.alliance.elo_mu
        appearance.elo_sigma_post = appearance.alliance.elo_sigma

    bulk_update(event.allianceappearance_set.all(), update_fields=['elo_mu_post', 'elo_sigma_post'])

    for team in event.teams.all():
        ranking = RankingModel.objects.get(team=team, event=event)
        ranking.elo_mu_post = team.elo_mu
        ranking.elo_sigma_post = team.elo_sigma
        ranking.save(update_fields=['elo_mu_post', 'elo_sigma_post'])

    print("Done!")


def soft_reset(value=SOFT_RESET_SCALE):
    Team.objects.exclude(elo_sigma=DEFAULT_SIGMA).update(
        elo_mu=F('elo_mu') - (F('elo_mu') - DEFAULT_MU) * value,
        elo_sigma=F('elo_sigma') - (F('elo_sigma') - DEFAULT_SIGMA) * value
    )
    Alliance.objects.exclude(elo_sigma=DEFAULT_SIGMA).update(
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
                for rank, team in enumerate(elo_leaders, start=1):
                    file.write("{3}\t{0}\t{1}\t{2}\n"
                               .format(str(team).replace("\t", ""), team.elo_scaled, team.elo_sigma, rank)
                               .replace('"', '\'\''))
                    # Replace double quotes so we can post it to Gist without Github freaking out
                    # Replace tab characters because Team 422 has a tab in their name (WHY?!)
                    # More teams have commas than tabs in their names so just uses .tsv file
        elif options['event'] == '':
            time_start = clock()
            if year == 0:
                years = [2015, 2016]
                for i in years:
                    add_all_elo(i)
                    if i != years[-1]:
                        soft_reset()
            else:
                add_all_elo(year)
            time_end = clock()
            print("-------------")
            print("Matches added:\t\t{0}".format(matches_added))
            print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
            print("-------------")
        else:
            # add_event_elo(Event.objects.get(key=options['event']))
            from cProfile import Profile
            profiler = Profile()
            profiler.runcall(add_event_elo, Event.objects.get(key=options['event']))
            profiler.print_stats(2)
