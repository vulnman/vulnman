<<<<<<< HEAD
from vulnman.api.viewsets import VulnmanModelViewSet
from apps.assets.api.v1 import serializers
from apps.assets import models


class TemplateViewSet(VulnmanModelViewSet):
    serializer_class = serializers.TemplateSerializer
    search_fields = ["name", "description", "resolution", "cve_id"]
    queryset = models.Template.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class VulnerabilityViewSet(VulnmanModelViewSet):
    serializer_class = serializers.VulnerabilitySerializer
    search_fields = ["name", "description", "resolution"]
    ignore_fields_after_creation = ["project", "host", "service", "hostname"]

    def get_queryset(self):
        return models.Vulnerability.objects.filter(
            project__creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
=======
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
>>>>>>> origin/dev
