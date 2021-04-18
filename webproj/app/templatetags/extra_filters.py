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


@register.filter(name='times')
def times(number):
    return range(number)


@register.simple_tag
def define(val=None):
    return val


class IncrementVarNode(template.Node):

    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        value = context[self.var_name]
        context[self.var_name] = value + 1
        return u""


@register.tag
def increment_var(parser, token):
    parts = token.split_contents()
    if len(parts) < 2:
        raise template.TemplateSyntaxError("'increment' tag must be of the form:  {% increment <var_name> %}")
    return IncrementVarNode(parts[1])

