from django.http import Http404
from rest_framework.permissions import DjangoObjectPermissions, SAFE_METHODS


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


class ObjectPermission(BaseObjectPermission):
    def has_object_permission(self, request, view, obj):
        # authentication checks have already executed via has_permission
        if view.get_permission_object():
            obj = view.get_permission_object()
            model_cls = obj._meta.model
        else:
            model_cls = self._get_queryset(view)
        perms = self.get_required_object_permissions(request.method, model_cls)
        user = request.user
        if not user.has_perms(perms, obj):
            # If the user does not have permissions we need to determine if
            # they have read permissions to see 403, or not, and simply see
            # a 404 response.

            if request.method in SAFE_METHODS:
                # Read permissions already checked and failed, no need
                # to make another lookup.
                raise Http404

            read_perms = self.get_required_object_permissions('GET', model_cls)
            if not user.has_perms(read_perms, obj):
                raise Http404
            # Has read permissions.
            return False
        return True

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only):
            return False

        if view.get_permission_object():
            model_cls = view.get_permission_object()._meta.model
        else:
            queryset = self._queryset(view)
            model_cls = queryset.model
        perms = self.get_required_permissions(request.method, model_cls)
        return request.user.has_perms(perms)
