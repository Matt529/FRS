from TBAW.models import Team, Event, Match, Alliance


def team_exists(team_number):
    return Team.objects.filter(team_number=team_number).exists()


def event_exists(event_key):
    return Event.objects.filter(key=event_key).exists()


def match_exists(event_key, match_key):
    event = Event.objects.get(key=event_key)
    return Match.objects.filter(key=match_key, event=event).exists()


def alliance_exists(teams):
    if type(teams[0]) is int:
        teams = [Team.objects.get(team_number=x) for x in teams]

    set1 = set(Alliance.objects.filter(teams__team_number=teams[0].team_number))
    set2 = set(Alliance.objects.filter(teams__team_number=teams[1].team_number))
    set3 = set(Alliance.objects.filter(teams__team_number=teams[2].team_number))
    return len(list(set1 & set2 & set3)) > 0


def event_has_f3_match(event_key):
    return Match.objects.filter(comp_level__exact='f', match_number__exact=3, event__key__exact=event_key).exists()
