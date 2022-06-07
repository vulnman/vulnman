from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import PermissionDenied
from api.v1.permissions import ProjectPermission
from apps.projects.models import Project


class ProjectPermissionRequiredMixin(object):
    object_permissions_required = None

    def get_permission_classes(self):
        if ProjectPermission not in self.permission_classes:
            return ImproperlyConfigured("ProjectPermission class not set")
        return super().get_permission_classes()

    def get_object_permissions_required(self):
        if not self.object_permissions_required:
            return None
        return self.object_permissions_required.copy()


class ProjectSessionAPIMixin(object):
    """
    This mixin adds a project from the session to the context
    of different viewset related mixins like CreateModelMixin
    """

    def get_project(self):
        """
        Get a project pk from the session
        """
        if not self.request.session.get("project_pk"):
            raise PermissionDenied
        return Project.objects.get(pk=self.request.session.get("project_pk"))

    def perform_create(self, serializer):
        """
        Overwrite CreateModelMixin to store project and creator
        of the object.
        """
        serializer.save(project=self.get_project(), creator=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.get_project()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(project=self.get_project())
