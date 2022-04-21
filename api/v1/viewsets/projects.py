from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import get_objects_for_user
from vulnman.api.viewsets import VulnmanModelViewSet
from apps.projects import models
from api.v1.serializers import project as serializers


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

    @action(detail=True, methods=['get'])
    def vulns_by_severity(self, request, pk=None):
        serializer = serializers.StatsVulnsBySeveritySerializer(
            instance=self.get_object(),
            data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=200)
        return Response(serializer.errors, 400)

    @action(detail=True, methods=['get'])
    def hosts_by_services(self, request, pk=None):
        serializer = serializers.StatsHostsByServicesSerializer(
            instance=self.get_object(),
            data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=200)
        return Response(serializer.errors, 400)

    @action(detail=True, methods=['get'])
    def vuln_category_counts(self, request, pk=None):
        serializer = serializers.StatsVulnCategoryCountSerializer(
            instance=self.get_object(),
            data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=200)
        return Response(serializer.errors, 400)
