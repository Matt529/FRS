from FRS.settings import DEFAULT_MU, DEFAULT_SIGMA
from TBAW.models import Team, Alliance
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

        for a in Alliance.objects.all():
            a.elo_mu = DEFAULT_MU
            a.elo_sigma = DEFAULT_SIGMA
            a.save()
            try:
                print("reset {0}".format(a))
            except UnicodeEncodeError:
                print("reset {0}".format(a).encode('utf-8'))
