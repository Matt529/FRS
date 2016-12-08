from time import clock

from concurrent.futures import wait, ProcessPoolExecutor
from requests_futures.sessions import FuturesSession
import requests

from TBAW.requester import get_team_robots_history_json, team_history_url_template
from TBAW.models import Robot, Team
from django.core.management.base import BaseCommand
from django.conf import settings
from util.atomics import AtomicVar
from itertools import repeat

robots_created = AtomicVar(0)


def add_all_robots(robots) -> None:

    print("Registering all robots for all teams...")

    requester = FuturesSession(executor=ProcessPoolExecutor(30), session=requests.Session())
    api_key = settings.TBA_API_HEADERS

    robots_get = lambda tn: requester.get(team_history_url_template(team=tn), headers=api_key)

    teams = Team.objects.all()
    print("Starting %d HTTP requests to retrieve robot history data for each team, split between %d processes..." % (len(teams), requester.executor._max_workers))
    robots_futures = [robots_get(team.team_number) for team in teams]
    print("Waiting...")
    wait(robots_futures)
    print("Done!\n")

    robot_jsons = [f.result().json() for f in robots_futures]
    for args in zip(teams, robot_jsons, repeat(robots)):
        add_team_robots(*args)


def add_team_robots(team: Team, robots, all_robots_by_team) -> None:
    global robots_created

    known_robots = all_robots_by_team.get(team.id, set())
    for year in robots:
        if robots[year]['key'] in known_robots:
            print("Skipping {}'s {} robot ({}:'{}'). Already known.".format(team.team_number, year, robots[year]['key'], robots[year]['name']))
            continue
        robot = Robot.objects.create(year=robots[year]['year'], team=team, key=robots[year]['key'],
                                     name=robots[year]['name'])
        known_robots |= {robots[year]['key']}
        robots_created += 1
        print("Added {0}'s {1} robot: {2}".format(team.team_number, robot.year, robot.name).encode('utf-8'))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--team', dest='team_number', default=-1, type=int)

    def handle(self, *args, **options):
        team_num = options['team_number']
        time_start = clock()

        robot_objs = Robot.objects.all()
        robots = {}
        for robot in robot_objs:
            if robot.team_id in robots:
                robots[robot.team_id] |= {robot.key}
            else:
                robots[robot.team_id] = {robot.key}

        if team_num != -1:
            add_team_robots(Team.objects.get(team_number=team_num), get_team_robots_history_json(team_num), robots)
        else:
            add_all_robots(robots)
        time_end = clock()

        print("-------------")
        print("Byte strings are printed to ignore unicode characters in windows terminals.")
        print("-------------")
        print("Robots created:\t\t{0}".format(robots_created))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
