from django.core.management.base import BaseCommand
from matplotlib import pyplot as plt

from TBAW.models import Team


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--file', dest='f', default='', type=str)

    def handle(self, *args, **options):
        if options['f'] is '':
            elo_array = [t.elo_mu for t in Team.objects.exclude(elo_mu=1500.0).order_by('id')]
            id_array = [t.id for t in Team.objects.exclude(elo_mu=1500.0).order_by('id')]
        else:
            pass  # implement read from CSV

        plt.scatter(id_array, elo_array)
        plt.show()
