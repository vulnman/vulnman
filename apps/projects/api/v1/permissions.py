from rest_framework.permissions import BasePermission
from apps.projects.models import Project


class AddContributorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.get_project().creator:
            return True
        return False

    def has_permission(self, request, view):
        if request.method == 'POST':
            project = request.data.get('project')
            instance = Project.objects.filter(pk=project, creator=request.user)
            if instance.exists():
                return True
            return False
        return True
