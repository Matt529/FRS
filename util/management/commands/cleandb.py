from django.core.management.base import BaseCommand

from TBAW.models import Team, Alliance, Event, ScoringModel, Match


class Command(BaseCommand):
    def handle(self, *args, **options):
        sure = input('Are you sure (Y/N)? ')
        if sure in ['y', 'Y']:
            Team.objects.all().delete()
            Alliance.objects.all().delete()
            Event.objects.all().delete()
            ScoringModel.objects.all().delete()
        elif sure == 'm':
            Match.objects.all().delete()
            ScoringModel.objects.all().delete()
            Team.objects.update(match_wins_count=0, match_losses_count=0, match_ties_count=0)