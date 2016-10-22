from time import clock

from django.core.management.base import BaseCommand

from FRS.settings import SUPPORTED_YEARS
from TBAW.models import Event, RankingModel
from TBAW.requester import get_event_statistics_json, get_event_rankings_json, get_teams_at_event
from util.data_logger import log_bad_data
from util.getters import get_event, get_instance_ranking_model, get_team

events_added = 0
teams_added = 0
teams_skipped = 0


def add_all(year: int) -> None:
    events = Event.objects.filter(year=year)
    for event in events:
        add_event_new(event.key)


def add_event(key: str) -> None:
    global teams_added, events_added, teams_skipped
    print("({1}) Adding stats for event {0}...".format(key, events_added + 1), flush=True)
    stats = get_event_statistics_json(key)
    rankings = get_event_rankings_json(key)
    event = get_event(key)
    model = get_instance_ranking_model(int(key[:4]))
    teams = get_teams_at_event(key)

    for team in teams:
        if RankingModel.objects.filter(event=event, team=team).exists():
            # print("Skipping team {0} (already exists)".format(team))
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
            # print("Skipping team {0} (can't find OPR/DPR/CCWMS)".format(team))
            teams_skipped += 1

        new_model.setup(rankings)
        new_model.save()
        event.rankingmodel_set.add(new_model)

        teams_added += 1

    events_added += 1


def add_event_new(key: str) -> None:
    """
    Needs testing -- RankingModel objects need new setup functions. Once tested and the old add_event function is
    removed, this should run in O(n) rather than O(n^2).

    Args:
        key: an event key
    """
    global teams_skipped, teams_added, events_added
    stats = get_event_statistics_json(key)
    rankings = get_event_rankings_json(key)
    event = get_event(key)
    model = get_instance_ranking_model(int(key[:4]))
    flag_2013 = False

    if not rankings or len(rankings) == 1:  # for cmp events since they don't have any rankings
        for team in event.teams.all():
            if model.objects.filter(team=team, event=event).exists():
                teams_skipped += 1
                continue

            new_model = model.objects.create()
            new_model.team = team
            new_model.tba_opr = 0
            new_model.tba_dpr = 0
            new_model.tba_ccwms = 0
            new_model.save()
            event.rankingmodel_set.add(new_model)
            teams_added += 1

        events_added += 1
        return

    for ranking_data in rankings[1:]:
        team_num = ranking_data[1]
        team = get_team(team_number=int(team_num))
        if RankingModel.objects.filter(event=event, team=team).exists():
            teams_skipped += 1
            continue

        try:
            if "HP" in rankings[0]:
                flag_2013 = True
            opr = stats['oprs']['{}'.format(team_num)]
            dpr = stats['dprs']['{}'.format(team_num)]
            ccwms = stats['ccwms']['{}'.format(team_num)]
        except (KeyError, IndexError):
            if event.event_code == 'cmp':
                opr = 0
                dpr = 0
                ccwms = 0
            else:
                print('skipping', flush=True)
                teams_skipped += 1
                log_bad_data('{} @ {}'.format(team_num, key), 'Cannot find OPR/DPR/CCWMS')
                continue

        if flag_2013:
            ranking_data.remove("0")  # Week 1 events in 2013 seem to have different API returns from TBA
        new_model = model.objects.create()
        new_model.team = team
        new_model.tba_opr = opr
        new_model.tba_dpr = dpr
        new_model.tba_ccwms = ccwms
        new_model.setup(ranking_data)
        new_model.save()
        event.rankingmodel_set.add(new_model)
        teams_added += 1

    if event.rankingmodel_set.count() != event.teams.count():
        for team in event.teams.all():
            if not event.rankingmodel_set.filter(team=team).exists():
                new_model = model.objects.create()
                new_model.team = team
                new_model.tba_opr = 0
                new_model.tba_dpr = 0
                new_model.tba_ccwms = 0
                new_model.save()
                event.rankingmodel_set.add(new_model)
                teams_added += 1

    events_added += 1
    print('Added {}'.format(key), flush=True)


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
            add_event_new(key)
        else:
            if year == 0:
                for yr in SUPPORTED_YEARS:
                    add_all(yr)
            else:
                add_all(year)
        time_end = clock()
        print("-------------")
        print("Events added:\t\t{0}".format(events_added))
        print("Teams added:\t\t{0}".format(teams_added))
        print("Teams skipped:\t\t{0}".format(teams_skipped))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
