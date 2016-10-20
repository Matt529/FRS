from django.test import TestCase
from .requester import get_team_json, get_event_json
from .models import Team, Event

import collections
import requests_mock
from TBAW.resource_getter import Requester, AsyncRequester, HttpMethod, ResourceResult

# save() is intentionally left out of setUp() methods, see Django docs

UrlTestParams = collections.namedtuple('UrlTestParams', ['url', 'method', 'kwargs'])

@requests_mock.Mocker()
class AsyncRequestTestCase(TestCase):

    def setUp(self):
        self.test_urls = {
            'GET': [
                UrlTestParams('http://www.test.com', HttpMethod.GET, {'text': 'Hello World!'}),
                UrlTestParams('http://www.tbaw.io', HttpMethod.GET, {'text': 'Wow look at all those robots!'})
            ],
            'POST': [
                UrlTestParams('http://www.tbaw.io', HttpMethod.POST, {'text': "Probably shouldn't..."})
            ],
            'HEAD': [
                UrlTestParams('http://www.frs.party', HttpMethod.HEAD, {'text': 'BYOR - Bring Your Own Robots'})
            ]
        }

    def _register_test_uris(self, mock: requests_mock.Mocker):
        for urls in self.test_urls.values():
            for url in urls:
                mock.register_uri(url.method.name, url.url, **url.kwargs)

    def test_instantiation(self):
        requester = Requester()
        async_requester = AsyncRequester()

        self.assertIsNotNone(requester, "Instantiation of synchronous resource getter failed.")
        self.assertIsNotNone(async_requester, "Instantiation of asynchronous resource getter failed.")
        self.assertIsInstance(async_requester, Requester,
                              "Asynchronous requester does not extend synchronous requester.")

    def test_synchronous_requests(self, mocker):
        self._register_test_uris(mocker)

        urls = self.test_urls['GET'] + self.test_urls['POST'] + self.test_urls['HEAD']
        urls = [(x.url, x.method) for x in urls]

        requester = Requester()
        requester.push_first(*urls[0])
        requester.push_first(*urls[1])
        requester.push_last(*urls[2])
        requester.push_last(*urls[3], identifier='party')

        import requests
        result = requester.retrieve('party')
        self.assertIsNotNone(result, 'Requester returns None for result on retrieve')
        self.assertIsInstance(result, ResourceResult, 'Requester does not return a Resource Result object')
        self.assertIsInstance(result.response, requests.Response, 'Result object does not contain a Response object')
        self.assertEqual(result.response.status_code, 200, 'Response Status was non-successful: %d' % result.response.status_code)
        self.assertEqual(result.response.text, 'Only information you need is that we party.', 'Incorrect text response')



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
