GROUP_PERMISSION_MAP = {
    "Management": {
        "permissions": {
            "projects.Project": [
                "add_project", "view_project", "change_project", "delete_project", "add_contributor",
                "add_client", "view_client", "change_client", "delete_client"],
        }
    },
    "Pentesters": {
        "permissions": {
            "projects.Project": ["add_project", "view_project", "change_project", "delete_project", "add_contributor"],
            "responsible_disc.Vulnerability": [
                "add_vulnerability", "view_vulnerability", "change_vulnerability", "delete_vulnerability",
                "invite_vendor", "add_comment"
            ]
        }
    },
    "Vendors": {
        "permissions": {
            "responsible_disc.Vulnerability": [
                "view_vulnerability", "add_comment"
            ]
        }
    }
}


def populate_groups_and_permission(sender, **kwargs):
    """
    Permissions are handled AFTER migration so this is the way to make it work with the tests

    :param sender:
    :param kwargs:
    :return:
    """
    from django.apps import apps
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    for group_key, group_value in GROUP_PERMISSION_MAP.items():
        group, _created = Group.objects.get_or_create(name=group_key)
        for perm_key in group_value.get("permissions", []):
            app_label, model_name = perm_key.split(".")
            model = apps.get_model(app_label, model_name)
            content_type = ContentType.objects.get_for_model(model)
            for perm in group_value["permissions"][perm_key]:
                permission, _created = Permission.objects.get_or_create(codename=perm, content_type=content_type)
                group.permissions.add(permission)
