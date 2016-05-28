from django.test import TestCase
from .TBAW_requester import make_team
from .models import Team


class TeamTestCase(TestCase):
    def setUp(self):
        test_teams = [1554, 2791]
        for test_team in test_teams:
            team_data = make_team(test_team)

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

            Team.objects.create(website=website, name=name, locality=locality, region=region,
                                country_name=country_name, location=location, key=key, nickname=nickname,
                                rookie_year=rookie_year, motto=motto, team_number=test_team)

    def test_contents(self):
        shaker = Team.objects.get(team_number=2791)
        self.assertEqual(shaker.motto, "K.I.S.S.")
        self.assertEqual(shaker.website, "http://www.team2791.org")
        self.assertEqual(shaker.nickname, "Shaker Robotics")
        self.assertEqual(shaker.locality, "Latham")
        self.assertEqual(shaker.region, "New York")
        self.assertEqual(shaker.country_name, "USA")
        self.assertEqual(shaker.location, "Latham, New York, USA")
        self.assertEqual(shaker.key, "frc2791")
        self.assertEqual(shaker.rookie_year, 2009)

        oceanside = Team.objects.get(team_number=1554)
        self.assertEqual(oceanside.motto, "Honor Above All")
        self.assertEqual(oceanside.website, "https://oceansiderobotics.wordpress.com/")
        self.assertEqual(oceanside.nickname, "Oceanside Robotics")
        self.assertEqual(oceanside.locality, "Oceanside")
        self.assertEqual(oceanside.region, "New York")
        self.assertEqual(oceanside.country_name, "USA")
        self.assertEqual(oceanside.location, "Oceanside, New York, USA")
        self.assertEqual(oceanside.key, "frc1554")
        self.assertEqual(oceanside.rookie_year, 2005)
