from django import template

register = template.Library()


@register.filter(name='get_team_rm')
def get_team_rm(ranking_models, team):
    return ranking_models.get(team=team)
