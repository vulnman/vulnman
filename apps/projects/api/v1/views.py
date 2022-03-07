from vulnman.api.viewsets import VulnmanModelViewSet, ProjectRelatedObjectViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from guardian.shortcuts import get_objects_for_user
from apps.projects import models
from apps.projects.api.v1 import serializers
from apps.projects.api.v1 import permissions


class ProjectViewSet(VulnmanModelViewSet):
    serializer_class = serializers.ProjectSerializer
    search_fields = ["name"]

    def get_queryset(self):
        # only get projects that we are allowed to see
        return get_objects_for_user(self.request.user, "projects.view_project", use_groups=False, with_superuser=False, 
            accept_global_perms=False, klass=models.Project)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=["patch"], url_path="archive-project", url_name="archive-project")
    def archive_project(self, request, pk=None):
        obj = self.get_object()
        serializer = serializers.ProjectArchiveSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            instance.archive_project()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectContributorViewSet(ProjectRelatedObjectViewSet):
    serializer_class = serializers.ProjectContributorSerializer
    permission_classes = [IsAuthenticated, permissions.AddContributorPermission]
    search_fields = ["user__username"]

    def get_queryset(self):
        return models.ProjectContributor.objects.all()
