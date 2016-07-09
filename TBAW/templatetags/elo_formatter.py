from django import template
from FRS.settings import SCALE

register = template.Library()


@register.filter(name='format_elo')
def format_elo(elo):
    return elo * SCALE
