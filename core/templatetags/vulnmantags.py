from django import template
from apps.findings.models import Template
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


@register.filter
def get_highest_severity_for_project(vulnerability_template, project):
    return vulnerability_template.get_highest_severity_for_project(project).get_severity_display()


@register.inclusion_tag("core/components/blankslate.html", takes_context=True)
def show_blankslate(context):
    return {
        'icon': context.get("blankslate_icon", "fa-exclamation"),
        'text': context.get('blankslate_text', 'Create a new instance with the button above!'),
        'title': context.get('blankslate_title', 'Nothing in here!')
    }


@register.inclusion_tag("core/components/navigation/breadcrumbs.html", takes_context=True)
def render_breadcrumbs(context):
    # render breadcrumbs from context
    return {
        'breadcrumbs': context.get("breadcrumbs")
    }
