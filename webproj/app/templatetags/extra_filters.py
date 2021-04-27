from django import template
from django.utils.safestring import mark_safe

from django.utils.encoding import force_text

register = template.Library()


@register.filter
def url_encode(value):
    return value.replace("/", "%2F")
