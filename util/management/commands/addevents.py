from datetime import date, timedelta
from time import clock

from django.core.management.base import BaseCommand

from FRS.settings import SUPPORTED_YEARS
from TBAW.models import Event, Alliance
from TBAW.requester import get_event_json, get_list_of_events_json
from util.check import event_exists, alliance_exists
from util.data_logger import log_bad_data
from util.getters import get_team, get_alliance

events_updated = 0
events_created = 0
events_skipped = 0

championship_keys = ['arc', 'cars', 'carv', 'gal', 'tes', 'new', 'cur', 'hop']


def add_list(year: int) -> None:
    events = get_list_of_events_json(year)
    for event_data in events:
        add_event(event_data['key'], get_event_json(event_data['key']))


def add_event(event_key: str, event_data=None) -> None:
    global events_updated, events_created, events_skipped
    if event_data is None:
        event_data = get_event_json(event_key)

    print("Adding event {0}".format(event_key))

    year = int(event_data['end_date'][:4])
    month = int(event_data['end_date'][5:7])
    day = int(event_data['end_date'][8:10])
    date_obj = date(year, month, day)

    # Make sure the date-based ordering of championship divisions and Einstein is correct by just moving divs up 1 day
    if event_key in championship_keys:
        date_obj -= timedelta(days=1)

    if event_exists(event_key):
        Event.objects.filter(key=event_key).update(name=event_data['name'], short_name=event_data['short_name'],
                                                   event_code=event_data['event_code'],
                                                   event_type=event_data['event_type'],
                                                   event_district=event_data['event_district'], year=event_data['year'],
                                                   location=event_data['location'],
                                                   venue_address=event_data['venue_address'],
                                                   timezone=event_data['timezone'], website=event_data['website'],
                                                   official=event_data['official'], end_date=date_obj)

        for alliance in event_data['alliances']:
            teams = [get_team(int(x[3:])) for x in alliance['picks']]
            if not alliance_exists(teams[0], teams[1], teams[2]):
                alliance_obj = Alliance.objects.create()
            else:
                alliance_obj = get_alliance(teams[0], teams[1], teams[2])

            for t in teams:
                alliance_obj.teams.add(t)

            alliance_obj.captain = teams[0]
            alliance_obj.first_pick = teams[1]
            alliance_obj.second_pick = teams[2]

            try:
                if alliance['backup'] is not None:
                    alliance_obj.backup = get_team(int(alliance['backup']['in'][3:]))
            except KeyError:
                pass

            alliance_obj.save()

        events_updated += 1
        # print("Updated event {0}".format(event_key))
    # We only want to analyze data from official events or IRI/Cheezy Champs
    elif (event_data['official'] is True and event_data['event_type_string'] != 'Offseason') or \
            event_data['event_code'] == 'iri':
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
                alliance_obj.teams.add(t)

            alliance_obj.captain = teams[0]
            alliance_obj.first_pick = teams[1]
            alliance_obj.second_pick = teams[2]

            if alliance['backup'] is not None:
                alliance_obj.backup = get_team(int(alliance['backup']['in'][3:]))

            alliance_obj.save()

        events_created += 1
        # print("Created event {0}".format(event_key))
    else:
        events_skipped += 1
        log_bad_data(event_key, 'Not an official event')
        print("Skipped event {0}".format(event_key))


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
                for yr in SUPPORTED_YEARS:
                    add_list(yr)
            else:
                add_list(year)
        time_end = clock()
        print("-------------")
        print("Events created:\t\t{0}".format(events_created))
        print("Events updated:\t\t{0}".format(events_updated))
        print("Events skipped:\t\t{0}".format(events_skipped))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
