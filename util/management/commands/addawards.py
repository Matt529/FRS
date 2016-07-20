from time import clock

from TBAW.models import Event, Award
from TBAW.requester import get_awards_from_event_json
from django.core.management.base import BaseCommand
from util.getters import get_event, get_team

awards_created = 0


def add_single_event(event):
    global awards_created
    awards = get_awards_from_event_json(event.key)
    print("Adding awards from event {0}".format(event.key))

    for award in awards:
        event = get_event(award['event_key'])
        award_type = award['award_type']
        name = award['name']
        recipients = list()
        for recipient in award['recipient_list']:
            if recipient['team_number'] is None:
                continue

            recipients.append(get_team(recipient['team_number']))

        year = award['year']
        award_obj = Award.objects.create(name=name, award_type=award_type, event=event, year=year)
        for recipient in recipients:
            award_obj.recipients.add(recipient)

        awards_created += 1


def add_all_events(year):
    for event in Event.objects.filter(year=year):
        add_single_event(event)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--key', dest='key', default='', type=str)
        parser.add_argument('--year', dest='year', default=2016, type=int)

    def handle(self, *args, **options):
        key = options['key']
        year = options['year']
        time_start = clock()
        if key is not '':
            add_single_event(key)
        else:
            add_all_events(year)
        time_end = clock()
        print("-------------")
        print("Awards created:\t\t{0}".format(awards_created))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
