from django import template
from django.utils.safestring import mark_safe

from django.utils.encoding import force_text

register = template.Library()


@register.filter
def get_product_with_index(l, i):
    try:
        return l[i]
    except:
        return None


