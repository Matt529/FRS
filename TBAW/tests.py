from django.test import TestCase
from .requester import get_team_json, get_event_json
from .models import Team, Event

import requests_mock
from util.templatestring import TemplateLike
from TBAW.resource_getter import Requester, AsyncRequester, HttpMethod, ResourceResult, make_resource_descriptor

# save() is intentionally left out of setUp() methods, see Django docs


class UrlTestParams(object):

    def __init__(self, url: TemplateLike, method: HttpMethod, mock_args: dict = None, *args, identifier: str = None):
        self.url = url
        self.method = method
        self.mock_args = mock_args or {}    # type: dict
        self.identifier = identifier

    def register_mock(self, mock: requests_mock.Mocker):
        mock.register_uri(self.method.name, self.url, **self.mock_args)

    def add_self_front(self, requester: Requester):
        self.identifier = requester.push_first(self.url, self.method, identifier=self.identifier)

    def add_self_back(self, requester: Requester):
        self.identifier = requester.push_last(self.url, self.method, identifier=self.identifier)

    def __str__(self):
        return 'UrlTest[%s as %s, %s]' % (self.url, self.identifier, self.mock_args)


@requests_mock.Mocker()
class NewRequesterTestCase(TestCase):

    def setUp(self):
        self.fixtures = [
            UrlTestParams('http://www.test.com', HttpMethod.GET, {'text': 'Hello World!'}),
            UrlTestParams('http://www.tbaw.io', HttpMethod.GET, {'text': 'Wow look at all those robots!'}),
            UrlTestParams('http://www.tbaw.io', HttpMethod.POST, {'text': "Probably shouldn't..."}),
            UrlTestParams('http://www.frs.party', HttpMethod.HEAD, {'text': 'BYOR - Bring Your Own Robots'}, identifier='party')
        ]

        self.GET_TEST_COM = self.fixtures[0]
        self.GET_TBAW_IO = self.fixtures[1]
        self.POST_TBAW_IO = self.fixtures[2]
        self.HEAD_FRS_PARTY = self.fixtures[3]

    def _register_test_uris(self, mock: requests_mock.Mocker):
        for url_params in self.fixtures:
            url_params.register_mock(mock)

    def test_instantiation(self, mocker):
        requester = Requester()
        async_requester = AsyncRequester()

        self.assertIsNotNone(requester, "Instantiation of synchronous resource getter failed.")
        self.assertIsNotNone(async_requester, "Instantiation of asynchronous resource getter failed.")
        self.assertIsInstance(async_requester, Requester,
                              "Asynchronous requester does not extend synchronous requester.")


    def test_synchronous_push(self, mocker):
        self._register_test_uris(mocker)

        requester = Requester()
        self.GET_TEST_COM.add_self_front(requester)
        self.POST_TBAW_IO.add_self_front(requester)

        self.assertEqual(len(requester), 2)

        self.GET_TBAW_IO.add_self_back(requester)
        self.HEAD_FRS_PARTY.add_self_back(requester)

        self.assertEqual(len(requester), 4)

    def test_synchronous_remove(self, mocker):
        requester = Requester()

        self.GET_TEST_COM.add_self_front(requester)
        self.POST_TBAW_IO.add_self_front(requester)
        self.GET_TBAW_IO.add_self_back(requester)
        self.HEAD_FRS_PARTY.add_self_back(requester)

        frs_party = requester.remove_last()
        self.assertIsInstance(frs_party, str)
        self.assertEqual(frs_party, self.HEAD_FRS_PARTY.identifier)

        tbaw_io_post = requester.remove_first()
        self.assertIsInstance(tbaw_io_post, str)
        self.assertEqual(tbaw_io_post, self.POST_TBAW_IO.identifier)

    def test_synchronous_requests(self, mocker):
        self._register_test_uris(mocker)

        requester = Requester()
        self.GET_TEST_COM.add_self_front(requester)
        self.POST_TBAW_IO.add_self_front(requester)
        self.GET_TBAW_IO.add_self_back(requester)
        self.HEAD_FRS_PARTY.add_self_back(requester)

        import requests
        first_test_fixture = self.HEAD_FRS_PARTY
        result = requester.retrieve(first_test_fixture.identifier)

        self.assertIsNotNone(result, 'Requester returns None for result on retrieve')
        self.assertIsInstance(result, ResourceResult, 'Requester does not return a Resource Result object')
        self.assertIsInstance(result.response, requests.Response, 'Result object does not contain a Response object')
        self.assertEqual(result.response.status_code, 200, 'Response Status was non-successful: %d' % result.response.status_code)
        self.assertEqual(result.response.text, first_test_fixture.mock_args['text'], 'Incorrect text response')

        with self.assertRaises(ValueError):
            requester.retrieve(first_test_fixture.identifier)

        results = requester.retrieve_all()
        self.assertIsInstance(results, dict, 'Requester did not return dictionary mapping strings to results.')
        for result in results.values():
            self.assertIsInstance(result, ResourceResult, 'Not all results from Requester are correct result type.')

        all_except_first = [x for x in self.fixtures if x != first_test_fixture]
        for fixture in all_except_first:
            self.assertTrue(fixture.identifier in results, "Resource '%s' (alias for '%s') did not appear in results although it should've!" % (fixture.identifier, fixture.url))

            result = results[fixture.identifier]

            self.assertIsInstance(result, ResourceResult, 'Requester does not return a Resource Result object')
            self.assertIsInstance(result.response, requests.Response, 'Result object does not contain a Response object')
            self.assertEqual(result.response.status_code, 200, 'Status code indicates failure')
            self.assertEqual(result.response.text, fixture.mock_args['text'], 'Incorrect text response')

        self.GET_TBAW_IO.add_self_front(requester)
        self.HEAD_FRS_PARTY.add_self_front(requester)

        tbaw_io = requester.remove_last()
        frs_party = requester.remove_first()

        with self.assertRaises(IndexError):
            requester.remove_first()
        with self.assertRaises(IndexError):
            requester.remove_last()

        self.assertIsInstance(tbaw_io, str)
        self.assertEqual(tbaw_io, self.GET_TBAW_IO.identifier)
        self.assertIsInstance(frs_party, str)
        self.assertEqual(frs_party, self.HEAD_FRS_PARTY.identifier)

        requester.push_all_first(*[make_resource_descriptor(x.url, x.method, identifier=x.identifier) for x in self.fixtures])
        self.assertEqual(len(self.fixtures), len(requester), 'Not all fixtures pushed onto requester queue')





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
