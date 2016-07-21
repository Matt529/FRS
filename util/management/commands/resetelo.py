from FRS.settings import DEFAULT_MU, DEFAULT_SIGMA
from TBAW.models import Team, Alliance
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        n = 0
        for t in Team.objects.all():
            t.elo_mu = DEFAULT_MU
            t.elo_sigma = DEFAULT_SIGMA
            t.save()
            n += 1
            try:
                print("({1}) reset {0}".format(t, n))
            except UnicodeEncodeError:
                print("({1}) reset {0}".format(t, n).encode('utf-8'))

        n = 0
        for a in Alliance.objects.all():
            a.elo_mu = DEFAULT_MU
            a.elo_sigma = DEFAULT_SIGMA
            a.save()
            n += 1
            try:
                print("({1}) reset {0}".format(a, n))
            except UnicodeEncodeError:
                print("({1}) reset {0}".format(a, n).encode('utf-8'))
