from vulnman.api.viewsets import VulnmanModelViewSet
from apps.findings.api.v1 import serializers
from apps.findings import models


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
