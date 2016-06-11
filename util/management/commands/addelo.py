from time import clock

from TBAW.models import Event
from django.core.management.base import BaseCommand
from leaderboard.models import TeamLeaderboard
from trueskill import Rating, rate

matches_added = 0


def handle_match_elo(match):
    global matches_added
    drawn = False
    if match.winner is None:
        drawn = True
        winners = match.alliances.all()[0].teams.all()
    else:
        winners = match.winner.teams.all()
    losers = [x for x in match.alliances.all() if x != match.winner][0].teams.all()
    winner_ts_pairs = [(t, Rating(t.elo_mu, t.elo_sigma)) for t in winners]
    loser_ts_pairs = [(t, Rating(t.elo_mu, t.elo_sigma)) for t in losers]
    if drawn:
        results = rate([[x[1] for x in winner_ts_pairs], [x[1] for x in loser_ts_pairs]], ranks=[0, 0])
    else:
        results = rate([[x[1] for x in winner_ts_pairs], [x[1] for x in loser_ts_pairs]])
    for winner_result, winner_team, loser_result, loser_team in zip(results[0], winners, results[1], losers):
        winner_team.elo_mu = winner_result.mu
        winner_team.elo_sigma = winner_result.sigma
        loser_team.elo_mu = loser_result.mu
        loser_team.elo_sigma = loser_result.sigma

        winner_team.save()
        loser_team.save()

    matches_added += 1
    print("({1}) Handled {0}".format(match, matches_added))


def add_all_elo():
    for event in Event.objects.exclude(key__in=['2016cmp', '2016cc']).order_by('end_date'):
        add_event_elo(event)

    add_event_elo(Event.objects.get(key='2016cmp'))
    add_event_elo(Event.objects.get(key='2016cc'))


def add_event_elo(event):
    for match in event.match_set.all():
        handle_match_elo(match)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--log', action='store_true', dest='log', default=False)

    def handle(self, *args, **options):
        log = options['log']
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

        else:
            time_start = clock()
            add_all_elo()
            time_end = clock()
            print("-------------")
            print("Matches added:\t\t{0}".format(matches_added))
            print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
            print("-------------")
