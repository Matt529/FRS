from typing import Iterable
from django.core.urlresolvers import reverse
from django.db.models import Model, Count

from util.strutils import TemplateString
from TBAW import models
from TBAW.models import Team, Event, Match, Alliance, ScoringModel2016, ScoringModel2015, \
    RankingModel2016, RankingModel2015, RankingModel2014, RankingModel2013, RankingModel2012, RankingModel2011, \
    RankingModel2010, ScoringModel, RankingModel
from django.conf import settings

import sys
import collections
from functools import reduce

def class_from_str(name: str):
    try:
        return reduce(getattr, name.split('.'), sys.modules[__name__])
    except:
        return None

__RANKING_MODEL_TEMPLATE = TemplateString("RankingModel{}")
__SCORING_MODEL_TEMPLATE = TemplateString("ScoringModel{}")

YEAR_TO_SCORING_MODEL = collections.OrderedDict()
YEAR_TO_RANKING_MODEL = collections.OrderedDict()

for year in settings.SUPPORTED_YEARS:
    ranking_model_t = class_from_str(__RANKING_MODEL_TEMPLATE(year))
    scoring_model_t = class_from_str(__SCORING_MODEL_TEMPLATE(year))

    if ranking_model_t is not None:
        YEAR_TO_RANKING_MODEL[year] = ranking_model_t
    if scoring_model_t is not None:
        YEAR_TO_SCORING_MODEL[year] = scoring_model_t


def get_teams(*team_numbers: Iterable[int]):
    return Team.objects.filter(id__in=list(team_numbers)).all()


def get_team(team_number: int) -> Team:
    """

    Args:
        team_number: a number associated with a team (e.g. 2791). can be type str or int.

    Returns:
        a Team object associated with the number

    """
    return Team.objects.get(id=team_number)


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
    return Alliance.objects.prefetch_related('teams').annotate(t=Count('teams')).filter(t=3, teams=team1).filter(teams=team2).get(teams=team3)


def get_instance_scoring_model(year: int) -> ScoringModel:
    """

    Args:
        year: The year that you want the scoring model for.

    Returns:
        An instance of ScoringModel relating to whatever year you want.

    """
    return YEAR_TO_SCORING_MODEL.get(year, ScoringModel)


def get_instance_ranking_model(year: int) -> RankingModel:
    """

    Args:
        year: The year you want the ranking model for.

    Returns:
        An instance of RankingModel relating to whatever year you want.

    """
    return YEAR_TO_RANKING_MODEL.get(year)


def make_team_table_row(name: str, url: str, holder: Model, stat) -> dict:
    return {
        'name': name,
        'url': url,
        'holder': holder,
        'holder_url': reverse_model_url(holder),
        'stat': stat
    }


def reverse_model_url(model: Model) -> str:
    if isinstance(model, models.Team):
        return reverse('team_view', kwargs={'team_number': model.team_number})
    elif isinstance(model, models.Event):
        return reverse('event_view', kwargs={'event_key': model.key})
    elif isinstance(model, models.Alliance):
        alliance = Alliance.objects.prefetch_related('teams').get(model.id)     # type: Alliance
        teams = alliance.teams.values('team_number').all()
        return reverse('alliance_view', kwargs={
            'team1': teams[0].team_number,
            'team2': teams[1].team_number,
            'team3': teams[2].team_number
        })
    elif isinstance(model, tuple(YEAR_TO_SCORING_MODEL.values())):
        return reverse('event_view', kwargs={
            'event_key': model.match_set.first().event.key
        })
    else:
        return ''
