from vulnman.api.viewsets import ProjectRelatedObjectViewSet, ProjectRelatedObjectListViewSet
from apps.assets import models
from apps.assets.api.v1 import serializers


class WebApplicationViewSet(ProjectRelatedObjectViewSet):
    queryset = models.WebApplication
    serializer_class = serializers.WebApplicationSerializer
    search_fields = ["name", "description", "base_url"]


class WebRequestViewSet(ProjectRelatedObjectViewSet):
    queryset = models.WebRequest
    serializer_class = serializers.WebRequestSerializer
    search_fields = ["web_app__name", "url", "parameter", "description"]


class HostViewSet(ProjectRelatedObjectViewSet):
    queryset = models.Host
    serializer_class = serializers.HostSerializer
    search_fields = ["ip", "description", "dns", "operating_system"]


class ServiceViewSet(ProjectRelatedObjectViewSet):
    queryset = models.Service
    serializer_class = serializers.ServiceSerializer
    search_fields = ["name"]
