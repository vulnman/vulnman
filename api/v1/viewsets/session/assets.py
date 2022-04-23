from apps.assets import models
from api.v1 import generics
from api.v1.serializers import assets as serializers


class HostViewSet(generics.SessionModelViewSet):
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()


class ServiceViewSet(generics.SessionModelViewSet):
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()


class WebApplicationViewSet(generics.SessionModelViewSet):
    serializer_class = serializers.WebApplicationSerializer
    queryset = models.WebApplication.objects.all()


class WebRequestViewSet(generics.SessionModelViewSet):
    serializer_class = serializers.WebRequestSerializer
    queryset = models.WebRequest.objects.all()
