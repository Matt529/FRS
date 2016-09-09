from django.core.management.base import BaseCommand

from util.generators import event_win_streaks


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        event_win_streaks()
