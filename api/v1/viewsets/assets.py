from api.v1 import generics
from api.v1.serializers import assets as serializers
from apps.assets import models


class AgentHostViewSet(generics.AgentModelViewSet):
    search_fields = ["ip", "dns"]
    serializer_class = serializers.AgentHostSerializer
    queryset = models.Host.objects.all()


class AgentServiceViewSet(generics.AgentModelViewSet):
    search_fields = ["host__ip", "name", "protocol", "port", "state"]
    serializer_class = serializers.AgentServiceSerializer
    queryset = models.Service.objects.all()
