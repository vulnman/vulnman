from rest_framework.filters import BaseFilterBackend
from guardian.shortcuts import get_objects_for_user


class ObjectPermissionsFilter(BaseFilterBackend):
    """
    Original Source: https://github.com/rpkilby/django-rest-framework-guardian/blob/master/src/rest_framework_guardian/filters.py
    Not maintained anymore!

    A filter backend that limits results to those where the requesting user
    has read object level permissions.
    """
    perm_format = '%(app_label)s.view_%(model_name)s'
    shortcut_kwargs = {
        'accept_global_perms': False
    }

    def filter_queryset(self, request, queryset, view):
        permission = self.perm_format % {
            'app_label': queryset.model._meta.app_label,
            'model_name': queryset.model._meta.model_name
        }
        return get_objects_for_user(request.user, permission, queryset, **self.shortcut_kwargs)


class ProjectRelatedObjectPermissionsFilter(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        project = queryset.get_project()
        perms = ["projects.view_project", "projects.change_project", "projects.delete_project"]
        has_permissions = all(self.request.user.has_perm(perm, project) for perm in perms)
        if has_permissions:
            pass
