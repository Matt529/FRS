from TBAW.models import Team, Event, Match, Alliance
from .getters import get_alliance


def team_exists(team_number):
    """

    Args:
        team_number: an int representation of a team (e.g. 2791, 3044)

    Returns:
        true if that team exists in the database, false otherwise

    """
    return Team.objects.filter(team_number=team_number).exists()


def event_exists(event_key):
    """

    Args:
        event_key: the year of the event and the string associated with the event (e.g. 2016nyro, 2014cmp, 2015iri)

    Returns:
        true if the event exists in the database, false otherwise

    """
    return Event.objects.filter(key=event_key).exists()


def match_exists(event_key, match_key):
    """

    Args:
        event_key: the year of the event and the string associated with the event (e.g. 2016nyro, 2014cmp, 2015iri)
        match_key: the year of the match, the event, the competition level of the match, the match number, and the set
        number, if applicable (e.g. 2016nyro_f1m1, 2015iri_sf2m2, 2015nytr_qm40).

    Returns:
        true if the match exists in the database, false otherwise

    """
    event = Event.objects.get(key=event_key)
    return Match.objects.filter(key=match_key, event=event).exists()


def alliance_exists(teams):
    """

    Args:
        teams: a list interpretation of teams, can be type int or type Team.

    Returns:
        true if the alliance exists in the database, false otherwise

    """
    if type(teams[0]) is int:
        teams = [Team.objects.get(team_number=x) for x in teams]

    set1 = set(Alliance.objects.filter(teams__team_number=teams[0].team_number))
    set2 = set(Alliance.objects.filter(teams__team_number=teams[1].team_number))
    set3 = set(Alliance.objects.filter(teams__team_number=teams[2].team_number))
    return len(list(set1 & set2 & set3)) > 0


def alliance_appearance_exists(alliance, event):
    if alliance_exists(list(alliance.teams.all())):
        alliance = get_alliance(list(alliance.teams.all()))
        return alliance.allianceappearance_set.filter(event=event).exists()
    else:
        return False


def event_has_f3_match(event_key):
    """

    Args:
        event_key: the year of the event and the string associated with the event (e.g. 2016nyro, 2014cmp, 2015iri)

    Returns:
        true if the event's finals set went to three games, false otherwise

    """
    return Match.objects.filter(comp_level__exact='f', match_number__exact=3, event__key__exact=event_key).exists()
