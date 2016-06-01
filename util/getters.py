from TBAW.models import Team, Event, Match
from .check import team_exists


def get_team(team_number):
    return Team.objects.get(team_number=team_number)


def get_previous_team(team_number):
    for num in range(team_number - 1, -1, -1):
        if num <= 0:
            return None
        if team_exists(num):
            return get_team(num)


def get_event(event_key):
    return Event.objects.get(key=event_key)


def get_match(event_key, match_key):
    return Match.objects.get(event_key=event_key, match_key=match_key)
