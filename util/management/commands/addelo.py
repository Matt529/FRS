from TBAW.models import Event
from django.core.management.base import BaseCommand


def handle_match_elo(match):
    drawn = False
    if match.winner is None:
        drawn = True
        winners = match.alliances.all()[0].teams.all()
    else:
        winners = match.winner.teams.all()
    losers = [x for x in match.alliances.all() if x != match.winner][0].teams.all()
    import trueskill
    winner_ts_pairs = [(t, trueskill.Rating(t.elo_mu, t.elo_sigma)) for t in winners]
    loser_ts_pairs = [(t, trueskill.Rating(t.elo_mu, t.elo_sigma)) for t in losers]
    if drawn:
        results = trueskill.rate([[x[1] for x in winner_ts_pairs], [x[1] for x in loser_ts_pairs]], ranks=[0, 0])
    else:
        results = trueskill.rate([[x[1] for x in winner_ts_pairs], [x[1] for x in loser_ts_pairs]])
    for winner_result, winner_team, loser_result, loser_team in zip(results[0], winners, results[1], losers):
        winner_team.elo_mu = winner_result.mu
        winner_team.elo_sigma = winner_result.sigma
        loser_team.elo_mu = loser_result.mu
        loser_team.elo_sigma = loser_result.sigma

        winner_team.save()
        loser_team.save()


def add_all_elo():
    for event in Event.objects.exclude(key='2016cmp').order_by('end_date'):
        add_event_elo(event)

    add_event_elo(Event.objects.get(key='2016cmp'))


def add_event_elo(event):
    for match in event.match_set.all():
        handle_match_elo(match)


class Command(BaseCommand):
    def handle(self, *args, **options):
        add_all_elo()
