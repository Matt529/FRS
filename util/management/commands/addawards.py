import functools
import itertools

from concurrent.futures import Future, wait
from typing import List, Dict
from time import clock

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db import transaction

from FRS.settings import SUPPORTED_YEARS
from TBAW.models import Event, Award
from TBAW.requester import get_awards_from_event_json, get_awards_from_event_json_async
from util.getters import get_event, get_team
from TBAW.resource_getter import AsyncRequester, ResourceResult

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

        if len(years) > 1:
            query = functools.reduce(lambda cur_q, next_year: cur_q | Q(year=next_year), years[1:], Q(year=years[0]))
        else:
            query = Q(year=year)

        requester = AsyncRequester(use_threads=False)
        event_futures = []  # type: List[Future]

        def create_handler(event):
            def handle(future):
                add_single_event(event, future.result().response.json())
            return handle

        for event in Event.objects.filter(query):
            event_futures.append(get_awards_from_event_json_async(requester, event.key))
            event_futures[-1].add_done_callback(create_handler(event))
            print("Requesting json data for event: {}".format(event.key))

        wait(event_futures)
