from django import template

register = template.Library()


@register.filter
def get_project_role(project, user):
    qs = project.projectcontributor_set.filter(user=user)
    if qs.exists():
        return qs.get().get_role_display()
    return
