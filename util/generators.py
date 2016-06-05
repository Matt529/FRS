from TBAW.models import Team


def non_championship_teams(year):
    return Team.objects.exclude(
        event__event_code__in=['cmp', 'arc', 'cur', 'cars', 'carv', 'gal', 'hop', 'new', 'tes']).filter(
        event__year=year).distinct()
