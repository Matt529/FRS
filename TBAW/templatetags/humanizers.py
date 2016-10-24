from django import template

register = template.Library()

comp_level_dict = {
    'qm': 'Qualifying',
    'ef': 'Eighth-final',
    'qf': 'Quarterfinal',
    'sf': 'Semifinal',
    'f': 'Final',
}


@register.filter(name='match_humanize')
def match_humanize(value):
    return comp_level_dict.get(value, default="Unknown")
