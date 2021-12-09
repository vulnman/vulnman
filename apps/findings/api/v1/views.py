from vulnman.api.viewsets import VulnmanModelViewSet
from apps.findings.api.v1 import serializers
from apps.findings import models


class TemplateViewSet(VulnmanModelViewSet):
    serializer_class = serializers.TemplateSerializer
    search_fields = ["name", "description", "remediation"]
    queryset = models.Template.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
