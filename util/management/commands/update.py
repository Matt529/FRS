from django.core.management.base import BaseCommand

from FRS.settings import LEADERBOARD_COUNT
from TBAW.models import Team, Event
from leaderboard2.models import TeamLeaderboard, ScoringLeaderboard2015, ScoringLeaderboard2016
from util import generators
from util.getters import get_instance_scoring_model


def event_stats_temp():
    excluded_events = ['cmp', 'cur', 'arc', 'carv', 'cars', 'gal', 'hop', 'new', 'tes', 'iri']
    teams = Team.objects.all()
    for team in teams:
        num_events = Event.objects.exclude(event_code__in=excluded_events).filter(teams=team).count()
        num_event_victories = Event.objects.exclude(event_code__in=excluded_events).filter(
            winning_alliance__teams=team).count()

        if num_events == 0:
            continue

        winrate = num_event_victories / num_events
        team.event_attended_count = num_events
        team.event_wins_count = num_event_victories
        team.event_winrate = winrate

    Team.objects.bulk_update(teams, update_fields=['event_attended_count', 'event_wins_count', 'event_winrate'])


def populate_team_leaderboards():
    if TeamLeaderboard.objects.count() > 0:
        TeamLeaderboard.objects.all().delete()

    team_leaderboards = generators.make_team_leaderboards()
    for tlb in team_leaderboards:
        tlb.save()
        qs = tlb.annotate_queryset(Team.objects.all())
        tlb.teams.set(qs.order_by('-ret_field')[:LEADERBOARD_COUNT])


def populate_scoring_leaderboards():
    ScoringLeaderboard2015.objects.all().delete()
    ScoringLeaderboard2016.objects.all().delete()

    scoring_leaderboards = generators.make_scoring_leaderboards()
    for slb in scoring_leaderboards:
        slb_year = int(slb.__class__.__name__[-4:])
        slb.save()
        qs = slb.annotate_queryset(get_instance_scoring_model(slb_year).objects.all())
        slb.scoring_models.set(qs.order_by('-ret_field')[:LEADERBOARD_COUNT])


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Team.objects.all().update(event_winrate=0.0, event_wins_count=0, match_winrate=0.0)
        # handle_event_winners()
        event_stats_temp()  # Event winners is broken and I don't know why. temporary rewrite. :)
        generators.event_win_streaks()
        populate_team_leaderboards()
        populate_scoring_leaderboards()
