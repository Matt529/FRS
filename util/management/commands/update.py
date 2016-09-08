from django.core.management.base import BaseCommand

from util.generators import win_streaks


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        streak = win_streaks()

