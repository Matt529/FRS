from TBAW.models import Team, Event


def team_exists(team_number):
    return Team.objects.filter(team_number=team_number).exists()


def event_exists(event_key):
    return Event.objects.filter(key=event_key).exists()
