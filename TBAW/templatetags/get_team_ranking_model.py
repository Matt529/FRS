from django import template
from typing import Dict

from TBAW.models.rankings import RankingModel
from TBAW.models.primitives import Team

register = template.Library()


@register.filter(name='get_team_rm')
def get_team_rm(ranking_models: Dict[int, RankingModel], team: Team):
    return ranking_models[team.team_number]
