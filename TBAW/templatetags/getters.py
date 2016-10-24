from typing import TypeVar, Dict, Any
from django import template

from django.conf import settings
from util.getters import reverse_model_url

register = template.Library()

T = TypeVar('T')


@register.filter(name='get_from_dict')
def get_from_dict(dictionary: Dict[T, Any], key: T):
    value = dictionary.get(key)

    if settings.DEBUG and value is None:
        print(key, dictionary)

    return value


@register.filter(name='url_finder')
def url_finder(obj):
    return reverse_model_url(obj)


@register.filter(name="get_model_url")
def get_model_url(obj):
    return url_finder(obj)
