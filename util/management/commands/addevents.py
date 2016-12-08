from typing import Iterable
from datetime import date, timedelta
from time import clock

from django.core.management.base import BaseCommand
from django.conf import settings

from concurrent.futures import wait, ProcessPoolExecutor
from requests_futures.sessions import FuturesSession
import requests

from FRS.settings import SUPPORTED_YEARS
from TBAW.models import Event, Alliance, AllianceAppearance
from TBAW.requester import get_event_json, get_list_of_events_json
from TBAW.requester import event_by_year_url_template, event_url_template, event_teams_url_template
from util.check import event_exists, alliance_exists, alliance_appearance_exists
from util.data_logger import log_bad_data
from util.getters import get_team, get_alliance

events_updated = 0
events_created = 0
events_skipped = 0

championship_keys = ['arc', 'cars', 'carv', 'gal', 'tes', 'new', 'cur', 'hop']

def add_all(*years: Iterable[int]):
    years = [*years]

    requester = FuturesSession(executor=ProcessPoolExecutor(30), session=requests.Session())
    api_key = settings.TBA_API_HEADERS

    event_list_get = lambda y: requester.get(event_by_year_url_template(year=y), headers=api_key)
    event_get = lambda key: requester.get(event_url_template(event=key), headers=api_key)
    event_teams_get = lambda key: requester.get(event_teams_url_template(event=key), headers=api_key)

    print("Getting event lists for years: %s" % years)
    event_list_futures = [event_list_get(y) for y in years]
    print("Waiting on %d requests..." % len(years))
    wait(event_list_futures)
    print("Done!\n")

    event_lists = [f.result().json() for f in event_list_futures]
    event_data_jsons = [item for year_data in event_lists for item in year_data]

    print("Grabbing event keys...")
    event_keys = [event_data['key'] for event_data in event_data_jsons]
    print("Starting %d requests for event data and teams-by-event data, split between %d processes..." % (2*len(event_keys), requester.executor._max_workers))
    event_json_futures = [event_get(key) for key in event_keys]
    event_team_json_futures = [event_teams_get(key) for key in event_keys]

    print("Waiting...")
    wait(event_json_futures + event_team_json_futures)
    requester.executor.shutdown()
    print("Done!\n")

    event_jsons = [f.result().json() for f in event_json_futures]
    event_team_json = [f.result().json() for f in event_team_json_futures]

    print("Adding teams data to event data under 'teams' field...")
    event_jsons = [dict(e, teams=t) for e, t in zip(event_jsons, event_team_json)]
    arg_list = zip(event_keys, event_jsons)

    for args in arg_list:
        add_event(*args)


def add_list(year: int) -> None:
    events = get_list_of_events_json(year)
    for event_data in events:
        add_event(event_data['key'], get_event_json(event_data['key']))


def add_event(event_key: str, event_data=None) -> None:
    global events_updated, events_created, events_skipped
    if event_data is None:
        event_data = get_event_json(event_key)

    year = int(event_data['end_date'][:4])
    month = int(event_data['end_date'][5:7])
    day = int(event_data['end_date'][8:10])
    date_obj = date(year, month, day)

    # Make sure the date-based ordering of championship divisions and Einstein is correct by just moving divs up 1 day
    if event_key in championship_keys:
        date_obj -= timedelta(days=1)

    if event_exists(event_key):
        print("Updating event {}".format(event_key))
        event = Event.objects.get(key=event_key)

        for alliance in event_data['alliances']:
            teams = [get_team(int(x[3:])) for x in alliance['picks']]
            if not alliance_exists(teams[0], teams[1], teams[2]):
                alliance_obj = Alliance.objects.create()
            else:
                alliance_obj = get_alliance(teams[0], teams[1], teams[2])

            for t in teams:
                if t not in alliance_obj.teams.all():
                    alliance_obj.teams.add(t)

            if not alliance_appearance_exists(alliance=alliance_obj, event=event):
                app = AllianceAppearance.objects.create(alliance=alliance_obj, event=event)
            else:
                continue

            app.captain = teams[0]
            app.first_pick = teams[1]
            app.second_pick = teams[2]

            try:
                if alliance['backup'] is not None:
                    app.backup = get_team(int(alliance['backup']['in'][3:]))
            except KeyError:
                pass

            app.save()

        events_updated += 1
        # print("Updated event {0}".format(event_key))

    # We only want to analyze data from official events or IRI/Cheezy Champs
    elif (event_data['official'] is True and event_data['event_type_string'] != 'Offseason') or \
            event_data['event_code'] == 'iri':
        print("Adding event {}".format(event_key))
        event = Event.objects.create(key=event_key, name=event_data['name'], short_name=event_data['short_name'],
                                     event_code=event_data['event_code'], event_type=event_data['event_type'],
                                     event_district=event_data['event_district'], year=event_data['year'],
                                     location=event_data['location'], venue_address=event_data['venue_address'],
                                     timezone=event_data['timezone'], website=event_data['website'],
                                     official=event_data['official'], end_date=date_obj)
        event.save()
        # Add the teams at creation time. Don't update the team list at update time due to time cost
        teams = event_data['teams']
        for t in teams:
            team = get_team(t['team_number'])
            event.teams.add(team)
            team.event_attended_count += 1
            team.save()

        for alliance in event_data['alliances']:
            teams = [get_team(int(x[3:])) for x in alliance['picks']]
            if not alliance_exists(teams[0], teams[1], teams[2]):
                alliance_obj = Alliance.objects.create()
            else:
                alliance_obj = get_alliance(teams[0], teams[1], teams[2])

            for t in teams:
                if t not in alliance_obj.teams.all():
                    alliance_obj.teams.add(t)

            if not alliance_appearance_exists(alliance=alliance_obj, event=event):
                app = AllianceAppearance.objects.create(alliance=alliance_obj, event=event)
            else:
                continue

            app.captain = teams[0]
            app.first_pick = teams[1]
            app.second_pick = teams[2]

            try:
                if alliance['backup'] is not None:
                    app.backup = get_team(int(alliance['backup']['in'][3:]))
            except KeyError:
                pass

            app.save()

        events_created += 1
        # print("Created event {0}".format(event_key))
    else:
        events_skipped += 1
        log_bad_data(event_key, 'Not an official event')
        print("Skipped event {0}, you aren't a REAL event.".format(event_key))


class Command(BaseCommand):
    help = "Adds events to the database"

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
            if year == 0:
                add_all(*SUPPORTED_YEARS)
                # for yr in SUPPORTED_YEARS:
                #     add_list(yr)
            else:
                add_all(year)
        time_end = clock()
        print("-------------")
        print("Events created:\t\t{0}".format(events_created))
        print("Events updated:\t\t{0}".format(events_updated))
        print("Events skipped:\t\t{0}".format(events_skipped))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
