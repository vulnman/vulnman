from api.core import viewsets
from apps.findings import models
from apps.findings.api.v1 import serializers


class VulnerabilityViewSet(viewsets.AgentModelViewSet):
    queryset = models.Vulnerability.objects.all()
    search_fields = ["name", "template__vulnerability_id"]
    serializer_class = serializers.VulnerabilitySerializer


class TextProofViewSet(viewsets.AgentModelViewSet):
    search_fields = ["text", "description"]
    serializer_class = serializers.TextProofSerializer

    def get_queryset(self):
        return models.TextProof.objects.filter(vulnerability__project=self.request.auth.project)
