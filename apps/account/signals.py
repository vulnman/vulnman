
def populate_groups_and_permission(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from apps.projects.models import Project
    management, _created = Group.objects.get_or_create(name="management")
    pentester, _created = Group.objects.get_or_create(name="pentester")
    content_type = ContentType.objects.get_for_model(Project)
    permission, _created = Permission.objects.get_or_create(codename="add_project", content_type=content_type)
    management.permissions.add(permission)
