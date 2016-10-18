from operator import itemgetter
from typing import List

import requests

from TBAW.models import Team
from util.templatestring import TemplateString
from util.getters import get_team

__api_key = {'X-TBA-App-Id': 'frs:frs:1'}
__tba_url = 'https://www.thebluealliance.com/api/v2/'

__team_template = TemplateString(__tba_url + 'team/frc{0}')
__team_history_template = __team_template + '/history/robots'
__team_participation_template = __team_template + '/years_participated'
__team_list_template = TemplateString(__tba_url + 'teams/{0}')
__event_by_year_template = TemplateString(__tba_url + 'events/{0}')
__event_template = TemplateString(__tba_url + 'event/{0}')
__event_ranking_template = __event_template + '/rankings'
__event_stats_template = __event_template + '/stats'
__event_teams_template = __event_template + '/teams'
__event_awards_template = __event_template + '/awards'
__event_matches_template = __event_template + '/matches'


# team_number is type int
def get_team_json(team_number: int) -> dict:
    url = __team_template(team_number)
    return requests.get(url, headers=__api_key).json()


def get_list_of_teams_json() -> List[dict]:
    teams = []
    for page in range(0, 13):
        url = __team_list_template(page)
        teams += requests.get(url, headers=__api_key).json()

    return teams


# event_key should be yyyyKEY, e.g. 2016nyro
def get_event_json(event_key: str) -> dict:
    url = __event_template(event_key)
    event_json = requests.get(url, headers=__api_key).json()

    url += '/teams'
    event_team_list_json = requests.get(url, headers=__api_key).json()
    event_teams = {'teams': event_team_list_json}

    # Merge two dictionaries
    return dict(event_json, **event_teams)


def get_list_of_events_json(year=2016) -> dict:
    url = __event_by_year_template(year)
    return requests.get(url, headers=__api_key).json()


def get_list_of_matches_json(event_key: str) -> List[dict]:
    url = __event_matches_template(event_key)
    json = requests.get(url, headers=__api_key).json()
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


def get_event_rankings_json(event_key: str) -> List[List[str]]:
    url = __event_ranking_template(event_key)
    return requests.get(url, headers=__api_key).json()


def get_event_statistics_json(event_key: str) -> dict:
    url = __event_stats_template(event_key)
    return requests.get(url, headers=__api_key).json()


def get_teams_at_event(event_key: str) -> List[Team]:
    url = __event_teams_template(event_key)
    teams = []
    teams_json = requests.get(url, headers=__api_key).json()
    for team in teams_json:
        teams.append(get_team(team['team_number']))

    return teams


def get_awards_from_event_json(event_key: str) -> List[dict]:
    url = __event_awards_template(event_key)
    return requests.get(url, headers=__api_key).json()


def get_team_robots_history_json(team_number: int) -> dict:
    url = __team_history_template(team_number)
    return requests.get(url, headers=__api_key).json()


def get_team_years_participated(team_number: int) -> List[int]:
    url = __team_participation_template(team_number)
    return requests.get(url, headers=__api_key).json()
