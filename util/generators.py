from typing import List

from django.db.models.query import QuerySet

from TBAW.models import Team, Event
from leaderboard2.models import TeamLeaderboard, ScoringLeaderboard2016

_CHAMPIONS = {
    'cmp',
    'arc',
    'cur',
    'cars',
    'carv',
    'gal',
    'hop',
    'new',
    'tes'
}

_CHAMPIONS_AND_IRI = _CHAMPIONS | {'iri'}


def non_championship_teams(year: int) -> QuerySet:
    """

    Args:
        year: The year that you want to get teams that didn't go to championships

    Returns:
        A QuerySet (django.db.models.QuerySet) that contains Team objects of teams that did not attend the
        championship event in the given year.
    """
    return Team.objects.exclude(event__event_code__in=_CHAMPIONS).filter(event__year=year).distinct()


def event_win_streaks() -> None:
    teams = Team.objects.all()
    for team in teams:
        streak = 0
        active_streak = 0
        excluded_events = _CHAMPIONS_AND_IRI
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


def make_team_leaderboards() -> List[TeamLeaderboard]:
    return [
        TeamLeaderboard(
            description="Elo Rating",
            field_1="-elo_mu"
        ),
        TeamLeaderboard(
            description="Active Event Winstreak (Excludes IRI and Championships)",
            field_1="-active_event_winstreak"
        ),
        TeamLeaderboard(
            description="Longest Event Winstreak (Excludes IRI and Championships)",
            field_1="-longest_event_winstreak"
        ),
        TeamLeaderboard(
            description="Most Event Wins",
            field_1="-event_wins_count"
        ),
        TeamLeaderboard(
            description="Highest Event Winrate",
            field_1="-event_winrate"
        ),
        TeamLeaderboard(
            description="Most Match Wins",
            field_1="-match_wins_count"
        ),
        TeamLeaderboard(
            description="Highest Match Winrate",
            field_1="-match_winrate"
        ),
        TeamLeaderboard(
            description="Most Awards",
            field_1="-awards_count"
        ),
        TeamLeaderboard(
            description="Most Blue Banners",
            field_1="-blue_banners_count"
        ),
    ]


def make_scoring_2016_leaderboards() -> List[ScoringLeaderboard2016]:
    return [
        ScoringLeaderboard2016(
            description='Highest Overall Score',
            field_1='-red_total_score',
            field_2='-blue_total_score',
            operator=ScoringLeaderboard2016.GREATEST
        ),
        ScoringLeaderboard2016(
            description='Highest Teleop Score',
            field_1='-red_teleop_score',
            field_2='-blue_teleop_score',
            operator=ScoringLeaderboard2016.GREATEST
        ),
        ScoringLeaderboard2016(
            description='Highest Autonomous Score',
            field_1='-red_auton_score',
            field_2='-blue_auton_score',
            operator=ScoringLeaderboard2016.GREATEST
        ),
    ]
