from datetime import date, timedelta
from time import clock

from TBAW.models import Event
from TBAW.requester import get_event_json, get_list_of_events_json
from django.core.management.base import BaseCommand
from util.check import event_exists
from util.getters import get_team

events_updated = 0
events_created = 0
events_skipped = 0

championship_keys = ['arc', 'cars', 'carv', 'gal', 'tes', 'new', 'cur', 'hop']


def add_list(year):
    events = get_list_of_events_json(year)
    for event_data in events:
        add_event(event_data['key'], get_event_json(event_data['key']))


def add_event(event_key, event_data=None):
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
        events_updated += 1
        # print("Updated event {0}".format(event_key))
    # We only want to analyze data from official events or IRI/Cheezy Champs
    elif (event_data['official'] is True and event_data['event_type_string'] != 'Offseason') or \
            event_data['event_code'] == 'iri' or event_data['event_code'] == 'cc':
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
            event.teams.add(get_team(t['team_number']))

        events_created += 1
        # print("Created event {0}".format(event_key))
    else:
        events_skipped += 1
        print("Skipped event {0}".format(event_key))


class Command(BaseCommand):
    help = "Adds events to the database"

    def add_arguments(self, parser):
        parser.add_argument('--key', dest='key', default='', type=str)
        parser.add_argument('--year', dest='year', default=2016, type=int)

    def handle(self, *args, **options):
        key = options['key']
        year = options['year']
        time_start = clock()
        if key is not '':
            add_event(key)
        else:
            add_list(year)
        time_end = clock()
        print("-------------")
        print("Events created:\t\t{0}".format(events_created))
        print("Events updated:\t\t{0}".format(events_updated))
        print("Events skipped:\t\t{0}".format(events_skipped))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
