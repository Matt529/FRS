from django.test import TestCase
from .TBAW_requester import get_team_json, get_event_json
from .models import Team, Event


# save() is intentionally left out of setUp() methods, see Django docs


class TeamTestCase(TestCase):
    def setUp(self):
        test_teams = [1554, 2791]
        for test_team in test_teams:
            team_data = get_team_json(test_team)

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


class EventTestCase(TestCase):
    def setUp(self):
        event_keys = ['2016nyro']
        for event_key in event_keys:
            event_data = get_event_json(event_key)
            key = event_data['key']
            name = event_data['name']
            short_name = event_data['short_name']
            event_code = event_data['event_code']
            year = event_data['year']
            location = event_data['location']
            venue_address = event_data['venue_address']
            timezone = event_data['timezone']
            website = event_data['website']
            official = event_data['official']
            event_type = event_data['event_type']
            event_district = event_data['event_district']

            Event.objects.create(key=key, name=name, short_name=short_name, event_code=event_code, year=year,
                                 location=location, venue_address=venue_address, timezone=timezone, website=website,
                                 official=official, event_type=event_type, event_district=event_district)

    def test_contents(self):
        nyro = Event.objects.get(key='2016nyro')
        self.assertEqual(nyro.key, '2016nyro')
        self.assertEqual(nyro.year, 2016)
        self.assertEqual(nyro.get_event_type_display(), 'Regional')
        self.assertEqual(nyro.get_event_district_display(), 'No District')
        self.assertEqual(nyro.location, 'Rochester, NY, USA')
        self.assertEqual(nyro.venue_address, 'Gordon Field House\nRochester Institute of Technology\n149 Lomb Memorial'
                                             ' Drive\nRochester, NY 14623\nUSA')
        self.assertEqual(nyro.official, True)
