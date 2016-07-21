from time import clock

from TBAW.requester import get_event_statistics_json, get_event_rankings_json, get_teams_at_event
from TBAW.models import Event, RankingModel
from django.core.management.base import BaseCommand
from util.getters import get_event, get_instance_ranking_model

events_added = 0
teams_added = 0
teams_skipped = 0


def add_all(year):
    events = Event.objects.filter(year=year)
    for event in events:
        add_event(event.key)


def add_event(key):
    global teams_added, events_added, teams_skipped
    print("({1}) Adding stats for event {0}...".format(key, events_added + 1))
    stats = get_event_statistics_json(key)
    rankings = get_event_rankings_json(key)
    event = get_event(key)
    model = get_instance_ranking_model(int(key[:4]))
    teams = get_teams_at_event(key)

    for team in teams:
        if RankingModel.objects.filter(event=event, team=team).exists():
            print("Skipping team {0} (already exists)".format(team))
            teams_skipped += 1
            continue

        # print("({1}) Stats for {0}...".format(team, teams_added + 1).encode('utf-8'))
        new_model = model.objects.create()
        new_model.team = team
        new_model.save()

        try:
            opr = stats['oprs']['{0}'.format(team.team_number)]
            dpr = stats['dprs']['{0}'.format(team.team_number)]
            ccwms = stats['ccwms']['{0}'.format(team.team_number)]

            new_model.tba_opr = opr
            new_model.tba_dpr = dpr
            new_model.tba_ccwms = ccwms
        except KeyError:
            try:
                print("Skipping team {0} (can't find OPR/DPR/CCWMS)".format(team))
            except UnicodeEncodeError:
                pass
            teams_skipped += 1

        new_model.setup(rankings)
        new_model.save()
        event.rankingmodel_set.add(new_model)

        teams_added += 1

    events_added += 1


class Command(BaseCommand):
    help = "Adds event rankings/statistics to the database"

    def add_arguments(self, parser):
        parser.add_argument('--key', dest='key', default='', type=str)
        parser.add_argument('--year', dest='year', default=0, type=int)

    def handle(self, *args, **options):
        key = options['key']
        year = options['year']
        time_start = clock()
        if key is not '':
            add_event(key)
        else:
            add_all(year)
        time_end = clock()
        print("-------------")
        print("Events added:\t\t{0}".format(events_added))
        print("Teams added:\t\t{0}".format(teams_added))
        print("Teams skipped:\t\t{0}".format(teams_skipped))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
