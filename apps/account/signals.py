import yaml
import os
from django.conf import settings


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
    map_file_path = os.path.join(settings.BASE_DIR, "apps/account/permission_map.yaml")
    with open(map_file_path, "r") as f:
        try:
            content = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
    for group_item in content:
        group, _created = Group.objects.get_or_create(name=group_item["name"])
        permissions_items = group_item["permissions"]
        for permissions_item in permissions_items:
            app_label, model_name = permissions_item.split(".")
            model = apps.get_model(app_label, model_name)
            content_type = ContentType.objects.get_for_model(model)
            for permission_name in permissions_items[permissions_item]:
                permission, _created = Permission.objects.get_or_create(codename=permission_name,
                                                                        content_type=content_type)
                group.permissions.add(permission)
    return

