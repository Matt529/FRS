from operator import itemgetter
from concurrent.futures import Future, wait
from typing import List, Callable

import requests
from requests_futures.sessions import FuturesSession

from TBAW.models import Team
from util.getters import get_team
from util.templatestring import TemplateString

__async_requester = FuturesSession(max_workers=2, session=requests.Session())

__api_key = {'X-TBA-App-Id': 'frs:frs:1'}
__tba_url = 'https://www.thebluealliance.com/api/v2/'

team_url_template = TemplateString(__tba_url + 'team/frc{team}')
team_history_url_template = team_url_template + '/history/robots'
team_participation_url_template = team_url_template + '/years_participated'

team_by_page_url_template = TemplateString(__tba_url + 'teams/{page}')
event_by_year_url_template = TemplateString(__tba_url + 'events/{year}')

event_url_template = TemplateString(__tba_url + 'event/{event}')
event_ranking_url_template = event_url_template + '/rankings'
event_stats_url_template = event_url_template + '/stats'
event_teams_url_template = event_url_template + '/teams'
event_awards_url_template = event_url_template + '/awards'
event_matches_url_template = event_url_template + '/matches'


# team_number is type int
def get_team_json(team_number: int) -> dict:
    url = team_url_template(team=team_number)
    return requests.get(url, headers=__api_key).json()


def get_list_of_teams_json() -> List[dict]:
    teams = []
    for page in range(0, 13):
        url = team_by_page_url_template(page=page)
        teams += requests.get(url, headers=__api_key).json()

    return teams


# event_key should be yyyyKEY, e.g. 2016nyro
def get_event_json(event_key: str) -> dict:
    url = event_url_template(event=event_key)
    event_json = requests.get(url, headers=__api_key).json()

    url += '/teams'
    event_team_list_json = requests.get(url, headers=__api_key).json()
    event_teams = {'teams': event_team_list_json}

    # Merge two dictionaries
    return dict(event_json, **event_teams)


def get_event_json_async(event_key: str) -> Callable[[], dict]:
    url = event_url_template(event=event_key)
    print(url)
    event_json_future = __async_requester.get(url, headers=__api_key)

    url += '/teams'
    event_team_list_future = __async_requester.get(url, header=__api_key)

    result = None
    def wait_for_event_json() -> dict:
        global result
        if result is None:
            event_json = event_json_future.result().response.json()
            event_team_list_json = event_team_list_future.result().response.json()
            event_teams = {'teams': event_team_list_json}
            result = dict(event_json, **event_teams)
        return result

    return event_json_future, event_team_list_future


def get_list_of_events_json(year=2016) -> dict:
    url = event_by_year_url_template(year=year)
    return requests.get(url, headers=__api_key).json()


def list_of_matches_json_converter(json) -> List[dict]:
    qm = []
    ef = []
    qf = []
    sf = []
    f = []

    for match in json:
        if match['comp_level'] == 'qm':
            qm.append(match)
        elif match['comp_level'] == 'ef':
            ef.append(match)
        elif match['comp_level'] == 'qf':
            qf.append(match)
        elif match['comp_level'] == 'sf':
            sf.append(match)
        elif match['comp_level'] == 'f':
            f.append(match)
        else:
            raise ValueError("Can't determine the comp_level of this match:\n{0}".format(match))

    key = itemgetter('match_number')
    matches = sorted(qm, key=key) + sorted(ef, key=key) + sorted(qf, key=key) + sorted(sf, key=key) + sorted(f, key=key)

    return matches


def get_list_of_matches_json(event_key: str) -> List[dict]:
    url = event_matches_url_template(event=event_key)
    json = requests.get(url, headers=__api_key).json()
    return list_of_matches_json_converter(json)


def get_list_of_matches_json_async(event_key: str, callback, *callback_args) -> Future:
    url = event_matches_url_template(event=event_key)
    future = __async_requester.get(url, headers=__api_key)

    def handle_done(future: Future):
        response = future.result()    # type: requests.Response
        json = response.json()
        callback(*callback_args, list_of_matches_json_converter(json))

    future.add_done_callback(handle_done)
    return future


def get_event_rankings_json(event_key: str) -> List[List[str]]:
    url = event_ranking_url_template(event=event_key)
    return requests.get(url, headers=__api_key).json()


def get_event_statistics_json(event_key: str) -> dict:
    url = event_stats_url_template(event=event_key)
    return requests.get(url, headers=__api_key).json()


def get_teams_at_event(event_key: str) -> List[Team]:
    url = event_teams_url_template(event=event_key)
    teams = []
    teams_json = requests.get(url, headers=__api_key).json()
    for team in teams_json:
        teams.append(get_team(team['team_number']))

    return teams


def get_awards_from_event_json(event_key: str) -> List[dict]:
    url = event_awards_url_template(event=event_key)
    return requests.get(url, headers=__api_key).json()


def get_awards_from_event_json_async(event_key: str) -> Future:
    url = event_awards_url_template(event=event_key)
    return __async_requester.get(url, headers=__api_key)


def get_team_robots_history_json(team_number: int) -> dict:
    url = team_history_url_template(team=team_number)
    return requests.get(url, headers=__api_key).json()


def get_team_years_participated(team_number: int) -> List[int]:
    url = team_participation_url_template(team=team_number)
    return requests.get(url, headers=__api_key).json()
