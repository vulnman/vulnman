from rest_framework.permissions import BasePermission


class AddContributorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        perms = ["projects.add_contributor"]
        if not obj.get_project():
            return False
        has_permissions = all(request.user.has_perm(perm, obj.get_project()) for perm in perms)
        return has_permissions