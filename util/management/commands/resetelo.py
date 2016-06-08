from FRS.settings import DEFAULT_MU, DEFAULT_SIGMA
from TBAW.models import Team
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for t in Team.objects.all():
            t.elo_mu = DEFAULT_MU
            t.elo_sigma = DEFAULT_SIGMA
            t.save()
            try:
                print("reset {0}".format(t))
            except UnicodeEncodeError:
                print("reset {0}".format(t).encode('utf-8'))
