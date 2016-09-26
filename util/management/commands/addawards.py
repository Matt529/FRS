from time import clock

from django.core.management.base import BaseCommand

from FRS.settings import SUPPORTED_YEARS
from TBAW.models import Event, Award
from TBAW.requester import get_awards_from_event_json
from util.getters import get_event, get_team

awards_created = 0


def add_single_event(event: Event) -> None:
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
            recipient.awards_count += 1
            if award_obj.award_type in [t[0] for t in Award.blue_banner_choices]:
                recipient.blue_banners_count += 1

            recipient.save()

        awards_created += 1


def add_all_events(year: int) -> None:
    for event in Event.objects.filter(year=year):
        add_single_event(event)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--key', dest='key', default='', type=str)
        parser.add_argument('--year', dest='year', default=0, type=int)

    def handle(self, *args, **options):
        key = options['key']
        year = options['year']
        time_start = clock()
        if key is not '':
            add_single_event(Event.objects.get(key=key))
        else:
            if year == 0:
                for yr in SUPPORTED_YEARS:
                    add_all_events(yr)
            else:
                add_all_events(year)
        time_end = clock()
        print("-------------")
        print("Awards created:\t\t{0}".format(awards_created))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
