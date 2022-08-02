from django import template
from apps.findings.models import get_severity_by_int


register = template.Library()


@register.filter
def get_vulns_for_project(vulnerability_template, project):
    return project.vulnerability_set.filter(template=vulnerability_template).order_by('-severity')


@register.filter
def get_severity_name(severity):
    return get_severity_by_int(severity)
