from django.core.exceptions import ImproperlyConfigured
from api.v1.permissions import ProjectPermission


class ObjectPermissionRequiredMixin(object):
    object_permissions_required = None
    permission_object = None

    def get_object_permissions_required(self):
        if not self.object_permissions_required:
            raise ImproperlyConfigured()
        return self.object_permissions_required.copy()

    def get_permission_object(self):
        return self.permission_object


class ProjectPermissionRequiredMixin(object):
    """
    # legacy
    Check if user has proper proejct permissions
    """
    object_permissions_required = None

    def get_permission_classes(self):
        if ProjectPermission not in self.permission_classes:
            return ImproperlyConfigured()
        return super().get_permission_classes()

    def get_object_permissions_required(self):
        if not self.object_permissions_required:
            raise ImproperlyConfigured()
        return self.object_permissions_required.copy()
