from TBAW.models import Team


def non_championship_teams(year):
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
