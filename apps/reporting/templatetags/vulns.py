from django import template

register = template.Library()

@register.filter
def get_vulns_for_project(template, project):
    return project.vulnerability_set.filter(template=template).order_by('-cvss_score')
