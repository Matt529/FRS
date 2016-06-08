from django.core.management.base import BaseCommand
from leaderboard.tests import test_leaderboard


class Command(BaseCommand):
    def handle(self, *args, **options):
        test_leaderboard()
