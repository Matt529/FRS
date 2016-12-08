from typing import Dict, Iterable
from time import clock

from concurrent.futures import ProcessPoolExecutor, wait

from django.core.management.base import BaseCommand
from django.conf import settings

from requests_futures.sessions import FuturesSession
import requests

from FRS.settings import SUPPORTED_YEARS
from TBAW.models import Event, RankingModel
from TBAW.requester import event_stats_url_template, event_ranking_url_template, get_event_statistics_json, get_event_rankings_json
from util.atomics import AtomicVar
from util.data_logger import log_bad_data
from util.getters import get_instance_ranking_model, get_team

events_added = AtomicVar(0)
events_skipped = AtomicVar(0)
teams_added = AtomicVar(0)
teams_skipped = AtomicVar(0)


def add_all_new(rms: Dict[int, RankingModel], *years: Iterable[int]):
    years = [*years]

    print("Executing for years: %s" % years)

    requester = FuturesSession(executor=ProcessPoolExecutor(30), session=requests.Session())
    api_key = settings.TBA_API_HEADERS

    stats_get = lambda e: requester.get(event_stats_url_template(event=e), headers=api_key)
    rankings_get = lambda e: requester.get(event_ranking_url_template(event=e), headers=api_key)

    events = Event.objects.filter(year__in=years).all()

    print("Starting {} HTTP requests split between {} processes.".format(2*len(events), requester.executor._max_workers))
    stats_futures = [stats_get(e) for e in events]
    rankings_futures = [rankings_get(e) for e in events]

    print("Waiting for HTTP requests to return...")
    wait(stats_futures + rankings_futures)
    print("Done!\n")
    requester.executor.shutdown()

    get_json = lambda f: f.result().json()
    arg_list = zip(events, [rms]*len(events), map(get_json, stats_futures), map(get_json, rankings_futures))

    for args in arg_list:
        add_event_new(*args)


def add_event_new(event: Event, rms: Dict[int, RankingModel], stats, rankings) -> None:
    """
    Needs testing -- RankingModel objects need new setup functions. Once tested and the old add_event function is
    removed, this should run in O(n) rather than O(n^2).

    Args:
        key: an event key
    """
    global teams_skipped, teams_added, events_added, events_skipped
    key = event.key
    model = get_instance_ranking_model(int(key[:4]))
    flag_2013 = False

    if event.id in rms:
        print("Skipping RMs for {}".format(key))
        events_skipped += 1
        return

    if not rankings or len(rankings) == 1:  # for cmp events since they don't have any rankings
        for team in event.teams.all():
            if model.objects.filter(team_id=team.id, event_id=event.id).exists():
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

    rms = {rm.team.id: rm for rm in RankingModel.objects.select_related('team').filter(event_id=event.id).all()}
    for ranking_data in rankings[1:]:
        team_num = ranking_data[1]
        team = get_team(team_number=int(team_num))
        if team.id in rms:
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

        if flag_2013 and event.year == 2013:
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
        rms = {rm.event_id: rm for rm in RankingModel.objects.all()}
        if key is not '':
            add_event_new(key, rms, get_event_rankings_json(key), get_event_statistics_json(key))
        else:
            if year == 0:
                add_all_new(rms, *SUPPORTED_YEARS)
            else:
                add_all_new(rms, year)
        time_end = clock()
        print("-------------")
        print("Events added:\t\t{0}".format(events_added))
        print("Events skipped:\t\t{0}".format(events_skipped))
        print("Teams added:\t\t{0}".format(teams_added))
        print("Teams skipped:\t\t{0}".format(teams_skipped))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
