from django import template

from leaderboard2.models import Leaderboard

register = template.Library()


@register.assignment_tag
def show_leaderboard_categories():
    return Leaderboard.categories
