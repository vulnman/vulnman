from django import template
from django.template.loader import engines
from django.utils.safestring import mark_safe
from vulnman.utils.markdown import bleach_md


register = template.Library()


@register.filter
def md_to_html(field_name):
    return mark_safe(bleach_md(field_name))
