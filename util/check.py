from TBAW.models import Team, Event, Match


def team_exists(team_number):
    return Team.objects.filter(team_number=team_number).exists()


def event_exists(event_key):
    return Event.objects.filter(key=event_key).exists()


def match_exists(event_key, match_key):
    event = Event.objects.get(key=event_key)
    return Match.objects.filter(key=match_key, event=event).exists()
