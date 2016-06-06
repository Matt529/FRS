from TBAW.TBAW_requester import get_event_statistics_json, get_event_rankings_json, get_teams_at_event
from django.core.management.base import BaseCommand
from util.getters import get_event, get_instance_ranking_model


def add_all():
    pass


def add_event(key):
    print("Processing data for event {0}".format(key))
    stats = get_event_statistics_json(key)
    rankings = get_event_rankings_json(key)
    event = get_event(key)
    model = get_instance_ranking_model(int(key[:4]))
    teams = get_teams_at_event(key)

    for team in teams:
        print("Processing data for {0}... ".format(team), end='')
        new_model = model.objects.create()
        new_model.team = team
        new_model.save()

        opr = stats['oprs']['{0}'.format(team.team_number)]
        dpr = stats['dprs']['{0}'.format(team.team_number)]
        ccwms = stats['ccwms']['{0}'.format(team.team_number)]

        new_model.tba_opr = opr
        new_model.tba_dpr = dpr
        new_model.tba_ccwms = ccwms

        print('opr={0}, dpr={1}, ccwms={2}... '.format(opr, dpr, ccwms), end='')

        new_model.setup(rankings)
        new_model.save()
        event.rankingmodel_set.add(new_model)


class Command(BaseCommand):
    help = "Adds event rankings/statistics to the database"

    def add_arguments(self, parser):
        parser.add_argument('--key', dest='key', default='', type=str)

    def handle(self, *args, **options):
        key = options['key']

        if key is not '':
            add_event(key)
        else:
            add_all()
