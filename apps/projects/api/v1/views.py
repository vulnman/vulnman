
from vulnman.api.viewsets import VulnmanModelViewSet, ProjectRelatedObjectViewSet
from rest_framework.permissions import IsAuthenticated
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

    # def archive_project(self):


class ProjectContributorViewSet(ProjectRelatedObjectViewSet):
    serializer_class = serializers.ProjectContributorSerializer
    permission_classes = [IsAuthenticated, permissions.AddContributorPermission]
    
    def get_queryset(self):
        return models.ProjectContributor.objects.all()
