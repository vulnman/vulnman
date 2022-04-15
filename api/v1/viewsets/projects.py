from guardian.shortcuts import get_objects_for_user
from vulnman.api.viewsets import VulnmanModelViewSet
from apps.projects import models
from apps.projects.api.v1 import serializers


class ProjectViewSet(VulnmanModelViewSet):
    serializer_class = serializers.ProjectSerializer
    search_fields = ["name"]

    def get_queryset(self):
        # only get projects that we are allowed to see
        return get_objects_for_user(
                self.request.user, "projects.view_project",
                use_groups=False, with_superuser=False,
                accept_global_perms=False, klass=models.Project)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
