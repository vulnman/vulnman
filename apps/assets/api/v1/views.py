from api.core import viewsets
from apps.assets import models
from apps.assets.api.v1 import serializers


class HostViewSet(viewsets.AgentModelViewSet):
    search_fields = ["ip", "dns"]
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()


class ServiceViewSet(viewsets.AgentModelViewSet):
    search_fields = ["host__ip", "name", "protocol", "port", "state"]
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()
