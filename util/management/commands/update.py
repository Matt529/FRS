from django.core.management.base import BaseCommand

from FRS.settings import LEADERBOARD_COUNT
from TBAW.models import Team
from leaderboard2.models import TeamLeaderboard
from util import generators


def populate_team_leaderboards():
    if TeamLeaderboard.objects.count() > 0:
        TeamLeaderboard.objects.all().delete()

    team_leaderboards = generators.make_team_leaderboards()
    for tlb in team_leaderboards:
        tlb.save()
        print('Starting Team Leaderboard for "{}"... '.format(tlb.field), flush=True, end='')
        tlb.teams.set(Team.objects.order_by(tlb.field)[:LEADERBOARD_COUNT])
        print('finished'.format(tlb.field), flush=True)


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #  generators.event_win_streaks()
        populate_team_leaderboards()
