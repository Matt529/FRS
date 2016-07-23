from django.core.management.base import BaseCommand

from FRS.settings import DEFAULT_MU, DEFAULT_SIGMA
from TBAW.models import Team, Alliance, RankingModel


class Command(BaseCommand):
    def handle(self, *args, **options):
        Team.objects.update(elo_mu=DEFAULT_MU, elo_sigma=DEFAULT_SIGMA)
        Alliance.objects.update(elo_mu=DEFAULT_MU, elo_sigma=DEFAULT_SIGMA)
        RankingModel.objects.update(elo_mu_pre=0, elo_mu_post=0, elo_sigma_pre=0, elo_sigma_post=0)
