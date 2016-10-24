from typing import TypeVar, Dict, Any
from django import template

from django.conf import settings

register = template.Library()

T = TypeVar('T')


@register.filter(name='get_from_dict')
def get_from_dict(dictionary: Dict[T, Any], key: T):
    value = dictionary.get(key)

    if settings.DEBUG and value is None:
        print(key, dictionary)

    return value
