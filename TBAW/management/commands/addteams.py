from TBAW.TBAW_requester import get_list_of_teams
from TBAW.models import Team
from django.core.management.base import BaseCommand
from util.getters import get_previous_team


class Command(BaseCommand):
    help = "Adds multiple teams to the database"

    def handle(self, *args, **options):
        teams = get_list_of_teams()
        for team_data in teams:
            if team_data['name'] is None:
                continue

            website = team_data['website']
            name = team_data['name']
            locality = team_data['locality']
            region = team_data['region']
            country_name = team_data['country_name']
            location = team_data['location']
            key = team_data['key']
            nickname = team_data['nickname']
            motto = team_data['motto']
            team_number = team_data['team_number']

            # Handle empty rookie year data field
            rookie_year = team_data['rookie_year']
            if rookie_year is None:
                prev = get_previous_team(team_number)
                rookie_year = prev.rookie_year

            team = Team.objects.create(website=website, name=name, locality=locality, region=region,
                                       country_name=country_name, location=location, key=key, nickname=nickname,
                                       rookie_year=rookie_year, motto=motto, team_number=team_number)
            team.save()
            print("We succeeded on team {0}".format(team_data['team_number']))
