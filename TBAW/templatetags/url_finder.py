from django import template

from util.getters import reverse_model_url

register = template.Library()


@register.filter(name='url_finder')
def url_finder(obj):
    return reverse_model_url(obj)
