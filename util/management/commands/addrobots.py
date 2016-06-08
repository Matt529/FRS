from time import clock

from TBAW.TBAW_requester import get_team_robots_history
from TBAW.models import Robot, Team
from django.core.management.base import BaseCommand
from util.getters import get_team

robots_created = 0


def add_all_robots():
    for team in Team.objects.all():
        add_team_robots(team.team_number)


def add_team_robots(team_number):
    global robots_created
    robots = get_team_robots_history(team_number)
    team = get_team(team_number)
    for year in robots:
        if Robot.objects.filter(year=robots[year]['year'], team=team, key=robots[year]['key'],
                                name=robots[year]['name']).exists():
            continue
        robot = Robot.objects.create(year=robots[year]['year'], team=team, key=robots[year]['key'],
                                     name=robots[year]['name'])
        robots_created += 1
        print("Added {0}'s {1} robot: {2}".format(robot.team, robot.year, robot.name).encode('utf-8'))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--team', dest='team_number', default=-1, type=int)

    def handle(self, *args, **options):
        team_num = options['team_number']
        time_start = clock()
        if team_num != -1:
            add_team_robots(team_num)
        else:
            add_all_robots()
        time_end = clock()
        print("-------------")
        print("Robots created:\t\t{0}".format(robots_created))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
