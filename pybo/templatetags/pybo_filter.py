
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg
