from rest_framework import permissions
from apps.projects.models import Project


class HasProjectPermission(permissions.BasePermission):
    """
    Permission to only add items to projects you have permission too
    """
    def has_object_permission(self, request, view, obj):
        return obj.project.creator == request.user

    def has_permission(self, request, view):
        if request.method == 'POST':
            project = request.data.get('project')
            instance = Project.objects.filter(pk=project, creator=request.user)
            if instance.exists():
                return True
            return False
        return True
