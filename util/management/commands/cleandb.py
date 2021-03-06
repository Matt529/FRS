from django.core.management.base import BaseCommand
from django.core.management import call_command

from TBAW.models import Team, Alliance, Event, ScoringModel, Match, RankingModel, AllianceAppearance


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('reset_db')
        call_command('migrate')

        # sure = input('Are you sure (Y/N)? ')
        # if sure in ['y', 'Y']:
        #     Alliance.objects.all().delete()
        #     AllianceAppearance.objects.all().delete()
        #     # RankingModel.objects.filter(event__key='2013cama').delete()
        #     # Team.objects.all().delete()
        #     # Alliance.objects.all().delete()
        #     # Event.objects.all().delete()
        #     # ScoringModel.objects.all().delete()
        # elif sure == 'm':
        #     Match.objects.all().delete()
        #     ScoringModel.objects.all().delete()
        #     Team.objects.update(match_wins_count=0, match_losses_count=0, match_ties_count=0)
