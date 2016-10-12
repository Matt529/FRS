from django import template

register = template.Library()


@register.filter(name='subtract')
def subtract(minuend, subtrahend):
    return minuend - subtrahend
