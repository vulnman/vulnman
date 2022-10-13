from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from apps.projects import models
from apps.projects.api.ui import serializers


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: write tests
    serializer_class = serializers.ProjectSerializer
    search_fields = ["name"]

    def get_queryset(self):
        return models.Project.objects.for_user(self.request.user)

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
