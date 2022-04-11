from rest_framework.permissions import DjangoObjectPermissions, BasePermission
from rest_framework.permissions import SAFE_METHODS


class BaseObjectPermission(DjangoObjectPermissions):
    """
    Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class ProjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            perms = ["projects.view_project"]
        else:
            perms = [
                "projects.view_project", "projects.change_project",
                "projects.delete_project"
            ]
        has_permissions = all(
            request.user.has_perm(perm, request.auth.project) for perm in perms
        )
        return has_permissions
