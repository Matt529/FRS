from json import dumps
from typing import Dict

from django.db.models.query import QuerySet

from FRS.settings import STATICFILES_DIRS
from TBAW.models import Team, Event


def non_championship_teams(year: int) -> QuerySet:
    """

    Args:
        year: The year that you want to get teams that didn't go to championships

    Returns:
        A QuerySet (django.db.models.QuerySet) that contains Team objects of teams that did not attend the
        championship event in the given year.

    """
    return Team.objects.exclude(
        event__event_code__in=['cmp', 'arc', 'cur', 'cars', 'carv', 'gal', 'hop', 'new', 'tes']).filter(
        event__year=year).distinct()


def win_streaks() -> Dict[str, Dict[str, int]]:
    longest_streaks = {}
    active_streaks = {}
    active = True
    teams = Team.objects.all()
    for team in teams:
        key = team.team_number
        streak = 0
        active_streak = 0
        longest_streaks[key] = 0
        excluded_events = ['iri', 'cmp', 'new', 'cur', 'arc', 'gal', 'cars', 'tes', 'carv', 'hop']
        for event in Event.objects.exclude(event_code__in=excluded_events).filter(teams=team).order_by('-end_date'):
            if team in event.winning_alliance.teams.all():
                streak += 1
                if active:
                    active_streak += 1
            else:
                if streak > longest_streaks[key]:
                    longest_streaks[key] = streak
                streak = 0
                active = False

        if streak > longest_streaks[key]:
            longest_streaks[key] = streak

        active_streaks[key] = active_streak

    with open(STATICFILES_DIRS[0] + '\\global\\json\\streaks.json', 'w+') as f:
        f.write(dumps({'longest': longest_streaks, 'active': active_streaks}))

    return longest_streaks
