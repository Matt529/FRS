from time import clock

from django.core.management.base import BaseCommand
from django.conf import settings

from concurrent.futures import wait, ProcessPoolExecutor
from requests_futures.sessions import FuturesSession
import requests

from TBAW.models import Team
from TBAW.requester import get_list_of_teams_json, get_team_json, get_team_years_participated
from TBAW.requester import team_by_page_url_template, team_participation_url_template
from util.atomics import AtomicVar
from util.check import team_exists
from util.data_logger import log_bad_data
from util.getters import get_previous_team

teams_updated = AtomicVar(0)
teams_created = AtomicVar(0)
teams_skipped = AtomicVar(0)

teams_page_range = (0, 13)

def get_page_range():
    global teams_page_range

    min, max = teams_page_range
    api_key = settings.TBA_API_HEADERS

    print("Determine last page to download from, current range is pages %d to %d." % (min, max))
    data = requests.get(team_by_page_url_template(page=max), headers=api_key).json()
    if data == []:
        print("Max page is empty, reducing until a page is found...")
        while data == []:
            max -= 1
            print("Testing page %d" % max)
            data = requests.get(team_by_page_url_template(page=max), headers=api_key).json()
        print("Found new maximum: %d!" % max)
    else:
        print("Max page is non-empty, incrementing until empty page found...")
        while data != []:
            max += 1
            print("Testing page %d" % max)
            data = requests.get(team_by_page_url_template(page=max), headers=api_key).json()
        print("%d was empty, using %d as max page." % (max, max-1))
        max -= 1

    print("Using pages from %d to %d" % (min, max))
    return (min, max)

def add_list_new() -> None:
    requester = FuturesSession(executor=ProcessPoolExecutor(30), session=requests.session())
    api_key = settings.TBA_API_HEADERS

    team_list_get = lambda p: requester.get(team_by_page_url_template(page=p), headers=api_key)
    team_participation_get = lambda tn: requester.get(team_participation_url_template(team=tn), headers=api_key)

    page_range = get_page_range()

    print("\nStarting %d HTTP requests for team lists, split between %d processes..." % (page_range[1] - page_range[0], requester.executor._max_workers))
    team_list_futures = [team_list_get(p) for p in range(*page_range)]
    print("Waiting...")
    wait(team_list_futures)
    print("Done!\n")

    teams_lists = map(lambda f: f.result().json(),team_list_futures)
    teams_data = [item for page_data in teams_lists for item in page_data]
    team_numbers = [*map(lambda t: t['team_number'], teams_data)]

    print("Starting %d HTTP requests for team participation data, split between %d processes..." % (len(team_numbers), requester.executor._max_workers))
    team_participation_futures = [team_participation_get(tn) for tn in team_numbers]
    print("Waiting...")
    wait(team_participation_futures)
    print("Done!\n")

    team_participations = map(lambda f: f.result().json(), team_participation_futures)
    arg_list = zip(team_numbers, teams_data, team_participations)

    for args in arg_list:
        add_team(*args)



def add_list() -> None:
    teams = get_list_of_teams_json()
    for team_data in teams:
        add_team(team_data['team_number'], team_data=team_data)


def add_team(team_number: int, team_data=None, years_participated=None) -> None:
    global teams_updated, teams_created, teams_skipped
    if team_data is None:
        team_data = get_team_json(team_number)

    print("Adding team {0}".format(team_number))
    website = team_data['website']
    name = team_data['name']
    locality = team_data['locality']
    region = team_data['region']
    country_name = team_data['country_name']
    location = team_data['location']
    key = team_data['key']
    nickname = team_data['nickname']
    motto = team_data['motto']
    years_participated = years_participated or get_team_years_participated(team_number)

    # Sometimes teams have participated but have null records, for reasons unknown. Check if they were ever active.
    # examples: 146, 413
    if name is None:
        if len(years_participated) == 0:
            teams_skipped += 1
            log_bad_data('{}'.format(team_number), 'Zero years participated')
            print("Skipping %d, has never participated." % team_number)
            return

    # Handle empty rookie year data field by guessing that it's equal to the year of the team before it
    # may not be perfect but it's the best option we've got
    rookie_year = team_data['rookie_year']
    if rookie_year is None:
        prev = get_previous_team(team_number)
        rookie_year = prev.rookie_year

    # Update the team rather than create an entirely new db entry
    if team_exists(team_number):
        Team.objects.filter(team_number=team_number).update(website=website, name=name, locality=locality,
                                                            region=region, country_name=country_name, location=location,
                                                            key=key, nickname=nickname, rookie_year=rookie_year,
                                                            motto=motto, active_years=years_participated)
        teams_updated += 1
    # But if it doesn't exist, then create a new db entry
    else:
        team = Team.objects.create(id=team_number, website=website, name=name, locality=locality, region=region,
                                   country_name=country_name, location=location, key=key, nickname=nickname,
                                   rookie_year=rookie_year, motto=motto, team_number=team_number,
                                   active_years=years_participated)
        team.save()
        teams_created += 1


class Command(BaseCommand):
    help = "Adds multiple teams to the database"

    def add_arguments(self, parser):
        parser.add_argument('--team', dest='team_number', default=-1, type=int)

    def handle(self, *args, **options):
        team_num = options['team_number']
        print("Adding teams...")
        time_start = clock()
        if team_num != -1:
            add_team(team_number=team_num)
        else:
            add_list_new()
        time_end = clock()
        print("-------------")
        print("Teams created:\t\t{0}".format(teams_created))
        print("Teams updated:\t\t{0}".format(teams_updated))
        print("Teams skipped:\t\t{0}".format(teams_skipped))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
