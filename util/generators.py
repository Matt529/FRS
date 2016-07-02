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


def iri_2016_teams():
    teams = [16, 20, 27, 33, 45, 67, 71, 118, 133, 179, 195, 217, 225, 233, 234, 245, 330, 461, 494, 503, 624, 868, 910,
             1023, 1024, 1058, 1086, 1114, 1241, 1257, 1310, 1405, 1511, 1529, 1619, 1640, 1675, 1718, 1720, 1731, 1746,
             1747, 1806, 2013, 2052, 2056, 2338, 2451, 2468, 2481, 2502, 2590, 2614, 1771, 2826, 3015, 3130, 3314, 3481,
             3538, 3620, 3641, 3683, 3824, 4039, 4587, 4967, 5254, 5460]
    return Team.objects.filter(team_number__in=teams)


def iri_scout():
    teams = [16, 20, 27, 33, 45, 67, 71, 118, 133, 179, 195, 217, 225, 233, 234, 245, 330, 461, 494, 503, 624, 868, 910,
             1023, 1024, 1058, 1086, 1114, 1241, 1257, 1310, 1405, 1511, 1529, 1619, 1640, 1675, 1718, 1720, 1731, 1746,
             1747, 1806, 2013, 2052, 2056, 2338, 2451, 2468, 2481, 2502, 2590, 2614, 1771, 2826, 3015, 3130, 3314, 3481,
             3538, 3620, 3641, 3683, 3824, 4039, 4587, 4967, 5254, 5460]
    from leaderboard.models import TeamLeaderboard
    from django.db.models import F
    return TeamLeaderboard.highest_win_rate().filter(team_number__in=teams).annotate(
        score=F('elo_mu') * F('win_rate')).order_by('-score')
