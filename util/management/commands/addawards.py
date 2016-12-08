import functools

from typing import List
from time import clock

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q
from django.db import transaction

from concurrent.futures import wait, ProcessPoolExecutor
from requests_futures.sessions import FuturesSession
import requests

from FRS.settings import SUPPORTED_YEARS
from TBAW.models import Event, Award
from TBAW.requester import event_awards_url_template
from util.getters import get_team

awards_created = 0


def add_single_event(event: Event, award_json: List[dict]) -> None:
    global awards_created
    awards = award_json

    if len(awards) == 0:
        return

    # awards = get_awards_from_event_json(event.key)
    print("Adding awards from event {0}".format(event.key))

    if len(awards) > 1:
        query = functools.reduce(
            lambda cur_q, next_award: cur_q | Q(key=next_award['event_key']), awards[1:], Q(key=awards[0]['event_key'])
        )
    else:
        query = Q(key=awards[0]['event_key'])

    event_key_to_event = {event.key: event for event in Event.objects.filter(query)}

    for award in awards:
        event = event_key_to_event[award['event_key']]
        award_type = award['award_type']
        name = award['name']
        recipients = list()
        for recipient in award['recipient_list']:
            if recipient['team_number'] is None:
                continue

            recipients.append(get_team(recipient['team_number']))

        year = award['year']
        award_obj = Award.objects.create(name=name, award_type=award_type, event=event, year=year)
        with transaction.atomic():
            for recipient in recipients:
                award_obj.recipients.add(recipient)
                recipient.awards_count += 1
                if award_obj.award_type in [t[0] for t in Award.blue_banner_choices]:
                    recipient.blue_banners_count += 1
                recipient.save()

        awards_created += 1


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
                self.add_all_events(*SUPPORTED_YEARS)
            else:
                self.add_all_events(year)
        time_end = clock()
        print("-------------")
        print("Awards created:\t\t{0}".format(awards_created))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")

    def add_all_events(self, year: int, *args: List[int]):
        years = [year, *args]

        print("Executing for years: %s" % years)

        requester = FuturesSession(executor=ProcessPoolExecutor(30), session=requests.Session())
        api_key = settings.TBA_API_HEADERS

        events = Event.objects.filter(year__in=years).all()
        print("Starting %d HTTP requests to get awards data, split between %d processes..." % (len(events), requester.executor._max_workers))
        awards_futures = [requester.get(event_awards_url_template(event=e.key), headers=api_key) for e in events]
        print("Waiting...")
        wait(awards_futures)
        print("Done!\n")

        awards = map(lambda f: f.result().json(), awards_futures)

        for args in zip(events, awards):
            add_single_event(*args)
