import requests
from django.test import TestCase
from .models import Team


class TeamTestCase(TestCase):
    def setUp(self):
        team_number = 2791
        __api_key = {'X-TBA-App-Id': 'frs:frs:1'}
        __tba_url = 'https://www.thebluealliance.com/api/v2/'

        url = __tba_url + 'team/frc{0}'.format(team_number)
        req = requests.get(url, headers=__api_key)
        resp = req.json()

        website = resp['website']
        name = resp['name']
        locality = resp['locality']
        region = resp['region']
        country_name = resp['country_name']
        location = resp['location']
        key = resp['key']
        nickname = resp['nickname']
        rookie_year = resp['rookie_year']
        motto = resp['motto']

        Team.objects.create(website=website, name=name, locality=locality, region=region,
                            country_name=country_name, location=location, key=key, nickname=nickname,
                            rookie_year=rookie_year, motto=motto, team_number=team_number)

    def test_contents(self):
        shaker = Team.objects.get(team_number=2791)
        self.assertEqual(shaker.motto, "K.I.S.S.")
