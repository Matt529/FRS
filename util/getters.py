from django.core.urlresolvers import reverse
from django.db.models import Model

from TBAW import models
from TBAW.models import Team, Event, Match, Alliance, ScoringModel2016, ScoringModel2015, \
    RankingModel2016, \
    RankingModel2015, ScoringModel, RankingModel


def get_team(team_number: int) -> Team:
    """

    Args:
        team_number: a number associated with a team (e.g. 2791). can be type str or int.

    Returns:
        a Team object associated with the number

    """
    return Team.objects.get(team_number=team_number)


def get_previous_team(team_number: int) -> Team:
    """
    Used for attempting to guess rookie year when one isn't provided.

    Args:
        team_number: A team number associated with a team

    Returns:
        the first active team with a team number lower than the parameter (e.g. get...(2791) returns Team 2789)

    """
    for num in range(team_number - 1, -1, -1):
        if num <= 0:
            return None
        if Team.objects.filter(team_number=num).exists():
            return get_team(num)


def get_event(event_key: str) -> Event:
    """

    Args:
        event_key: a str containing a year and an event string (e.g. 2016nyro)

    Returns:
        The Event object associated with the event key

    """
    return Event.objects.get(key=event_key)


def get_match(event_key: str, match_key: str) -> Match:
    """

    Args:
        event_key: the year of the event and the string associated with the event (e.g. 2016nyro, 2014cmp, 2015iri)
        match_key: the year of the match, the event, the competition level of the match, the match number, and the set
        number, if applicable (e.g. 2016nyro_f1m1, 2015iri_sf2m2, 2015nytr_qm40).

    Returns:
        Match with the key match_key at Event with the key event_key.

    """
    return Match.objects.get(event_key=event_key, match_key=match_key)


def get_alliance(team1: Team, team2: Team, team3: Team) -> Alliance:
    """

    Args:
        team1: the first team of the alliance
        team2: the second team of the alliance
        team3: the third team of the alliance

    Returns:
        Alliance containing the three teams provided.

    """
    return Alliance.objects.filter(teams=team1).filter(teams=team2).get(teams=team3)


def get_instance_scoring_model(year: int) -> ScoringModel:
    """

    Args:
        year: The year that you want the scoring model for.

    Returns:
        An instance of ScoringModel relating to whatever year you want.

    """
    return {
        2016: ScoringModel2016,
        2015: ScoringModel2015,
        # etc
    }.get(year, ScoringModel)


def get_instance_ranking_model(year: int) -> RankingModel:
    """

    Args:
        year: The year you want the ranking model for.

    Returns:
        An instance of RankingModel relating to whatever year you want.

    """
    return {
        2016: RankingModel2016,
        2015: RankingModel2015,
        # etc
    }.get(year)


def make_team_tr(name: str, url: str, holder: Model, stat) -> dict:
    return {
        'name': name,
        'url': url,
        'holder': holder,
        'holder_url': reverse_model_url(holder),
        'stat': stat
    }


def reverse_model_url(model: Model) -> str:
    if type(model) is models.Team:
        return reverse('team_view', kwargs={'team_number': model.team_number})
    elif type(model) is models.Event:
        return reverse('event_view', kwargs={'event_key': model.key})
    elif type(model) is models.Alliance:
        return reverse('alliance_view', kwargs={
            'team1': model.teams.all()[0].team_number,
            'team2': model.teams.all()[1].team_number,
            'team3': model.teams.all()[2].team_number
        })
    elif type(model) in [ScoringModel2016, ScoringModel2015, ScoringModel]:
        return reverse('event_view', kwargs={
            'event_key': model.match_set.first().event.key
        })
    else:
        return ''
