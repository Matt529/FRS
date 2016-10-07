from django.core.management.base import BaseCommand

from FRS.settings import LEADERBOARD_COUNT
from TBAW.models import Team, ScoringModel2016
from leaderboard2.models import TeamLeaderboard, ScoringLeaderboard2016
from util import generators


def populate_team_leaderboards():
    if TeamLeaderboard.objects.count() > 0:
        TeamLeaderboard.objects.all().delete()

    team_leaderboards = generators.make_team_leaderboards()
    for tlb in team_leaderboards:
        tlb.save()
        qs = tlb.annotate_queryset(Team.objects.all())
        tlb.teams.set(qs.order_by('-ret_field')[:LEADERBOARD_COUNT])


def populate_scoring_leaderboards():
    if ScoringLeaderboard2016.objects.count() > 0:
        ScoringLeaderboard2016.objects.all().delete()

    scoring_leaderboards = generators.make_scoring_2016_leaderboards()
    for slb in scoring_leaderboards:
        slb.save()
        qs = slb.annotate_queryset(ScoringModel2016.objects.all())
        slb.scoring_models.set(qs.order_by('-ret_field')[:LEADERBOARD_COUNT])


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # generators.event_win_streaks()
        populate_team_leaderboards()
        populate_scoring_leaderboards()
