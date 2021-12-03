from vulnman.api import viewsets
from vulnman.api.permissions import HasProjectPermission
from rest_framework.permissions import IsAuthenticated
from apps.projects.api import serializers
from apps.projects import models


class ProjectViewSet(viewsets.CreateListRetrieveViewSet):
    permission_classes = [HasProjectPermission, IsAuthenticated]
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        return models.Project.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
