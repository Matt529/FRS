from TBAW.models import Team, Event, Match, Alliance, AllianceAppearance


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
    if type(teams[0]) is Team:
        teams = [t.team_number for t in teams]

    return Alliance.objects.filter(teams__team_number=teams[0]).filter(teams__team_number=teams[1]).filter(
        teams__team_number=teams[2]).exists()


def alliance_appearance_exists(alliance, event):
    return AllianceAppearance.objects.filter(alliance=alliance, event=event).exists()
