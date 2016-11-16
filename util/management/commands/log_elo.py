import os

from django.core.management.base import BaseCommand

from FRS.settings import BASE_DIR, DEFAULT_MU, DEFAULT_SIGMA
from TBAW.models import Team


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(BASE_DIR, 'logs\\elo\\elo_{}_{}.csv'.format(DEFAULT_MU, DEFAULT_SIGMA)), 'a+') as f:
            for t in Team.objects.exclude(elo_mu=1500.0).order_by('id'):
                f.write('{},{},{},{},{},{},{}\n'.format(t.team_number, t.rookie_year, t.match_wins_count,
                                                        t.match_losses_count, t.match_ties_count, t.elo_mu,
                                                        t.elo_sigma))
