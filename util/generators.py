from django.db.models.query import QuerySet

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


def event_win_streaks() -> None:
    teams = Team.objects.all()
    for team in teams:
        streak = 0
        active_streak = 0
        excluded_events = ['iri', 'cmp', 'new', 'cur', 'arc', 'gal', 'cars', 'tes', 'carv', 'hop']
        for event in Event.objects.exclude(event_code__in=excluded_events).filter(teams=team).order_by('end_date'):
            if team in event.winning_alliance.teams.all():
                streak += 1
                active_streak += 1
            else:
                if streak > team.longest_event_winstreak:
                    team.longest_event_winstreak = streak
                streak = 0
                active_streak = 0

        if streak > team.longest_event_winstreak:
            team.longest_event_winstreak = streak

        team.active_event_winstreak = active_streak

    Team.objects.bulk_update(teams, update_fields=['longest_event_winstreak', 'active_event_winstreak'])
