import requests
from .models import Event

__api_key = {'X-TBA-App-Id': 'frs:frs:1'}
__tba_url = 'https://www.thebluealliance.com/api/v2/'


# team_number is type int
def make_team(team_number):
    url = __tba_url + 'team/frc{0}'.format(team_number)
    req = requests.get(url, headers=__api_key)
    response = req.json()

    team = {
        'website': response['website'],
        'name': response['name'],
        'locality': response['locality'],
        'region': response['region'],
        'country_name': response['country_name'],
        'location': response['location'],
        'key': response['key'],
        'nickname': response['nickname'],
        'rookie_year': response['rookie_year'],
        'motto': response['motto'],
        'team_number': team_number,
    }

    return team


def get_list_of_teams():
    url = __tba_url + 'teams/0'
    return requests.get(url, headers=__api_key).json()


# event_key should be yyyyKEY, e.g. 2016nyro
def make_event(event_key):
    url = __tba_url + 'event/{0}'.format(event_key)
    req = requests.get(url, headers=__api_key)
    resp = req.json()

    name = resp['name']
    short_name = resp['short_name']
    event_code = resp['event_code']

    event_type = resp['event_type']
    event_district = resp['event_district']

    year = resp['year']
    location = resp['location']
    venue_address = resp['venue_address']
    timezone = resp['timezone']
    website = resp['website']
    official = resp['official']

    event = Event(event_key=event_key, name=name, short_name=short_name,
                  event_code=event_code, event_type=event_type, event_district=event_district,
                  year=year, location=location, venue_address=venue_address,
                  timezone=timezone, website=website, official=official)
    event.save()
