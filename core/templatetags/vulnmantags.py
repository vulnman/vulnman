from django import template
from urllib.parse import urlencode

register = template.Library()


@register.filter
def unique_url_params(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value
    what, to = arg.split('|')
    value[what] = to
    return urlencode(value)

