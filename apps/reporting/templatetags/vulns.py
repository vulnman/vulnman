from django import template

register = template.Library()


@register.filter
def get_vulns_for_project(vulnerability_template, project):
    return project.vulnerability_set.filter(template=vulnerability_template).order_by('-severity')
