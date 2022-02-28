from apps.networking.api.v1 import serializers
from apps.networking import models
from vulnman.api import viewsets


class HostViewSet(viewsets.VulnmanModelViewSet):
    serializer_class = serializers.HostSerializer
    search_fields = ["ip", "hostname__name"]
    ignore_fields_after_creation = ["project"]

    def get_queryset(self):
        return models.Host.objects.filter(project__creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ServiceViewSet(viewsets.VulnmanModelViewSet):
    serializer_class = serializers.ServiceSerializer
    search_fields = ["name", "protocol", "port", "banner"]
    ignore_fields_after_creation = ["project", "host"]

    def get_queryset(self):
        return models.Service.objects.filter(project__creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class HostnameViewSet(viewsets.VulnmanModelViewSet):
    serializer_class = serializers.HostnameSerializer
    search_fields = ["name", "host__ip"]
    ignore_fields_after_creation = ["host", "project"]

    def get_queryset(self):
        return models.Hostname.objects.filter(project__creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
