from TBAW.TBAW_requester import make_team
from TBAW.models import Team
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Adds a team to the database"

    def add_arguments(self, parser):
        parser.add_argument('team_number', nargs='+', type=int)

    def handle(self, *args, **options):
        for team_number in options['team_number']:
            if Team.objects.filter(team_number=team_number).exists():
                raise CommandError('Team {0} already exists'.format(team_number))
            else:
                team_data = make_team(team_number)

                website = team_data['website']
                name = team_data['name']
                locality = team_data['locality']
                region = team_data['region']
                country_name = team_data['country_name']
                location = team_data['location']
                key = team_data['key']
                nickname = team_data['nickname']
                rookie_year = team_data['rookie_year']
                motto = team_data['motto']

                team = Team.objects.create(website=website, name=name, locality=locality, region=region,
                                           country_name=country_name, location=location, key=key, nickname=nickname,
                                           rookie_year=rookie_year, motto=motto, team_number=team_number)
                team.save()
