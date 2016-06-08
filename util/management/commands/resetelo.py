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
        # with open('elo.txt', 'w', encoding='utf-8') as file:
        #     file.write("Rank\tTeam\tElo (initial 25)\n")
        #     for count, team in enumerate(Team.objects.filter(event__year=2016).distinct().order_by('-elo_mu'), start=1):
        #         file.write("{0}\t{1}\t{2}\n".format(count, team.__str__().replace('\t', ''), team.elo_mu * 60).replace("\"", '\'\''))
