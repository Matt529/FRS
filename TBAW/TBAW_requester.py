from .models import Team, Event
import requests

api_key = {'X-TBA-App-Id': 'frs:frs:1'}
tba_url = 'https://www.thebluealliance.com/api/v2/'


# team_number is type int
def make_team(team_number):
    url = tba_url + 'team/frc{0}'.format(team_number)
    req = requests.get(url, headers=api_key)
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

    team = Team(website=website, name=name, locality=locality, region=region, country_name=country_name,
                location=location, key=key, nickname=nickname, rookie_year=rookie_year, motto=motto,
                team_number=team_number)
    team.save()


# event_key should be yyyyKEY, e.g. 2016nyro
def make_event(event_key):
    url = tba_url + 'event/{0}'.format(event_key)
    req = requests.get(url, headers=api_key)
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
