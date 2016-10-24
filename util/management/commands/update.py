from django.core.management.base import BaseCommand

from FRS.settings import LEADERBOARD_COUNT
from TBAW.models import Team
from leaderboard2.models import TeamLeaderboard, ScoringLeaderboard2015, ScoringLeaderboard2016
from util import generators
from util.getters import get_instance_scoring_model
from util.management.commands.addmatches import handle_event_winners


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
        Team.objects.all().update(event_winrate=0.0, event_wins_count=0, match_winrate=0.0)
        handle_event_winners()
        # generators.event_win_streaks()
        populate_team_leaderboards()
        # populate_scoring_leaderboards()
