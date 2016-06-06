import requests
from util.getters import get_team

__api_key = {'X-TBA-App-Id': 'frs:frs:1'}
__tba_url = 'https://www.thebluealliance.com/api/v2/'


# team_number is type int
def get_team_json(team_number):
    url = __tba_url + 'team/frc{0}'.format(team_number)
    return requests.get(url, headers=__api_key).json()


def get_list_of_teams_json():
    teams = []
    for page in range(0, 13):
        url = __tba_url + 'teams/{0}'.format(page)
        teams += requests.get(url, headers=__api_key).json()

    return teams


# event_key should be yyyyKEY, e.g. 2016nyro
def get_event_json(event_key):
    url = __tba_url + 'event/{0}'.format(event_key)
    event_json = requests.get(url, headers=__api_key).json()

    url += '/teams'
    event_team_list_json = requests.get(url, headers=__api_key).json()
    event_teams = {'teams': event_team_list_json}

    # Merge two dictionaries
    return dict(event_json, **event_teams)


def get_list_of_events_json(year=2016):
    url = __tba_url + 'events/{0}'.format(year)
    return requests.get(url, headers=__api_key).json()


def get_list_of_matches_json(event_key):
    url = __tba_url + 'event/{0}/matches'.format(event_key)
    return requests.get(url, headers=__api_key).json()


def get_event_rankings_json(event_key):
    url = __tba_url + 'event/{0}/rankings'.format(event_key)
    return requests.get(url, headers=__api_key).json()


def get_event_statistics_json(event_key):
    url = __tba_url + 'event/{0}/stats'.format(event_key)
    return requests.get(url, headers=__api_key).json()


def get_teams_at_event(event_key):
    url = __tba_url + 'event/{0}/teams'.format(event_key)
    teams = []
    teams_json = requests.get(url, headers=__api_key).json()
    for team in teams_json:
        teams.append(get_team(team['team_number']))

    return teams
