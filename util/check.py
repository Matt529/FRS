from django.db.models import Count

from TBAW.models import Team, Event, Match, Alliance, AllianceAppearance

from typing import Callable
from types import BuiltinFunctionType


def is_builtin(fn: Callable) -> bool:
    return type(fn) is BuiltinFunctionType


def team_exists(team_number: int) -> bool:
    """

    Args:
        team_number: an int representation of a team (e.g. 2791, 3044)

    Returns:
        true if that team exists in the database, false otherwise

    """
    return Team.objects.filter(team_number=team_number).exists()


def event_exists(event_key: str) -> bool:
    """

    Args:
        event_key: the year of the event and the string associated with the event (e.g. 2016nyro, 2014cmp, 2015iri)

    Returns:
        true if the event exists in the database, false otherwise

    """
    return Event.objects.filter(key=event_key).exists()


def match_exists(event: Event, match_key: str) -> bool:
    """

    Args:
        event: Event associated with match (e.g. 2016nyro, 2014cmp, 2015iri)
        match_key: the year of the match, the event, the competition level of the match, the match number, and the set
        number, if applicable (e.g. 2016nyro_f1m1, 2015iri_sf2m2, 2015nytr_qm40).

    Returns:
        true if the match exists in the database, false otherwise

    """
    return Match.objects.filter(key=match_key, event_id=event.id).exists()


def alliance_exists(team1: Team, team2: Team, team3: Team) -> bool:
    """

    Args:
        team1: the first team of the alliance
        team2: the second team of the alliance
        team3: the third team of the alliance

    Returns:
        true if the alliance exists in the database, false otherwise

    """

    return Alliance.objects.annotate(t=Count('teams')).filter(t=3).filter(teams=team1).filter(teams=team2).filter(
        teams=team3).exists()


def alliance_appearance_exists(alliance: Alliance, event: Event) -> bool:
    return AllianceAppearance.objects.filter(alliance=alliance, event=event).exists()
