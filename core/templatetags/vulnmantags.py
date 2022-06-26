from django import template
from urllib.parse import urlencode

register = template.Library()


@register.filter
def unique_url_params(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if isinstance(value, str):
        return value
    if len(arg.split('|')) != 2:
        return value
    result = value.copy()
    what, to = arg.split('|')
    result[what] = to
    return urlencode(result)
