from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from guardian.shortcuts import get_objects_for_user
from apps.projects import models
from apps.api.v2.serializers import projects as serializers


class ProjectViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]
    serializer_class = serializers.ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        # only get projects that we are allowed to see
        return get_objects_for_user(
            self.request.user, "projects.view_project",
            use_groups=False, with_superuser=False,
            accept_global_perms=False, klass=models.Project)
