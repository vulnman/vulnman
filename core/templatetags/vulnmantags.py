from django import template
from django.utils.safestring import mark_safe
import bleach
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


@register.filter
def get_asset_link(asset):
    # prevent XSS here but we need to mark the return string as safe
    cleaned_asset = bleach.clean(str(asset))
    cleaned_type = bleach.clean(asset.asset_type)
    return mark_safe('<a href="{url}">{asset} ({asset_type})</a>'.format(
        url=asset.get_absolute_url(), asset=cleaned_asset, asset_type=cleaned_type))


@register.filter
def get_customer_link(customer):
    cleaned_name = bleach.clean(str(customer.name))
    return mark_safe('<a href="{url}">{name}</a>'.format(name=cleaned_name, url=customer.get_absolute_url()))
