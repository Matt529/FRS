from django import template

register = template.Library()


@register.filter(name='get_from_dict')
def get_from_dict(dictionary, key):
    return dictionary.get(key)
