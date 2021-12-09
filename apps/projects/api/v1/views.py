from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from dry_rest_permissions.generics import DRYPermissions
from apps.projects import models
from apps.projects.api.v1 import serializers


class ProjectViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [DRYPermissions, IsAuthenticated]
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        return models.Project.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
