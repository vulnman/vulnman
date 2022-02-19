from vulnman.api.viewsets import VulnmanModelViewSet
from vulnman.api.mixins import ProjectPermissionMixin
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
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


class ProofSetOrder(mixins.UpdateModelMixin, mixins.DestroyModelMixin, ProjectPermissionMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if models.TextProof.objects.filter(pk=self.kwargs.get("pk")).exists():
            return serializers.TextProofSerializer
        return serializers.ImageProofSerializer

    def get_queryset(self):
        if models.TextProof.objects.filter(pk=self.kwargs.get("pk")).exists():
            return models.TextProof.objects.filter(pk=self.kwargs.get("pk"))
        return models.ImageProof.objects.filter(pk=self.kwargs.get("pk"))

    