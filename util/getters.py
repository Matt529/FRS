from TBAW.models import Team, Event, Match, Alliance, ScoringModel2016, ScoringModel2015, ScoringModel2014, \
    RankingModel2016, RankingModel2015
from .check import team_exists


def get_team(team_number):
    if type(team_number) is not int:
        team_number = int(team_number)
    return Team.objects.get(team_number=team_number)


def get_previous_team(team_number):
    for num in range(team_number - 1, -1, -1):
        if num <= 0:
            return None
        if team_exists(num):
            return get_team(num)


def get_event(event_key):
    return Event.objects.get(key=event_key)


def get_match(event_key, match_key):
    return Match.objects.get(event_key=event_key, match_key=match_key)


def get_alliance(teams, event_key=None):
    if type(teams[0]) is int:
        teams = [Team.objects.get(team_number=x) for x in teams]
    set1 = set(Alliance.objects.filter(teams__team_number=teams[0].team_number))
    set2 = set(Alliance.objects.filter(teams__team_number=teams[1].team_number))
    set3 = set(Alliance.objects.filter(teams__team_number=teams[2].team_number))
    alliances = list(set1 & set2 & set3)
    for alliance in alliances:
        if event_key is not None:
            if alliance in get_event(event_key).alliances.all():
                return alliance
        else:
            if alliance.seed > 0:
                return alliance
    return alliances[0]


def get_instance_scoring_model(year):
    return {
        2016: ScoringModel2016,
        2015: ScoringModel2015,
        2014: ScoringModel2014,
        # etc
    }.get(year)


def get_instance_ranking_model(year):
    return {
        2016: RankingModel2016,
        2015: RankingModel2015,
        # etc
    }.get(year)
