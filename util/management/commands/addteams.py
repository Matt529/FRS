from time import clock

from TBAW.models import Team
from TBAW.requester import get_list_of_teams_json, get_team_json, get_team_years_participated
from django.core.management.base import BaseCommand
from util.check import team_exists
from util.getters import get_previous_team

teams_updated = 0
teams_created = 0
teams_skipped = 0


def add_list() -> None:
    teams = get_list_of_teams_json()
    for team_data in teams:
        add_team(team_data['team_number'], team_data=team_data)


def add_team(team_number: int, team_data=None) -> None:
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

    # Sometimes teams have null records, for reasons unknown. Check if null records were indeed ever active
    # examples: 146, 413
    if name is None:
        years_participated = get_team_years_participated(team_number)
        if len(years_participated) == 0:
            teams_skipped += 1
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
                                                            motto=motto)
        teams_updated += 1
        # print("Updated team {0}".format(team_number))
    # But if it doesn't exist, then create a new db entry
    else:
        team = Team.objects.create(website=website, name=name, locality=locality, region=region,
                                   country_name=country_name, location=location, key=key, nickname=nickname,
                                   rookie_year=rookie_year, motto=motto, team_number=team_number)
        team.save()
        teams_created += 1
        # print("Created team {0}".format(team_number))


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
            add_list()
        time_end = clock()
        print("-------------")
        print("Teams created:\t\t{0}".format(teams_created))
        print("Teams updated:\t\t{0}".format(teams_updated))
        print("Teams skipped:\t\t{0}".format(teams_skipped))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
