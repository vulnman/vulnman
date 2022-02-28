<<<<<<< HEAD
from vulnman.api.viewsets import VulnmanModelViewSet
from vulnman.api.mixins import ProjectPermissionMixin
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from apps.findings.api.v1 import serializers
=======
from vulnman.api.viewsets import ProjectRelatedObjectViewSet, GenericListRetrieveModelViewSet
>>>>>>> origin/dev
from apps.findings import models
from apps.findings.api.v1 import serializers


class UserAccountViewSet(ProjectRelatedObjectViewSet):
    queryset = models.UserAccount.objects.all()
    serializer_class = serializers.UserAccountSerializer


class TemplateViewSet(GenericListRetrieveModelViewSet):
    queryset = models.Template.objects.all()
    serializer_class = serializers.TemplateSerializer
    search_fields = ["name", "vulnerability_id", "description"]


class ProofViewSet(ProjectRelatedObjectViewSet):
    def get_queryset(self):
        if models.TextProof.objects.filter(pk=self.kwargs.get("pk")).exists():
            return models.TextProof.objects.filter(pk=self.kwargs.get("pk"))
        return models.ImageProof.objects.filter(pk=self.kwargs.get("pk"))
    
    def get_serializer_class(self):
        if models.TextProof.objects.filter(pk=self.kwargs.get("pk")).exists():
            return serializers.TextProofSerializer
        return serializers.ImageProofSerializer

<<<<<<< HEAD
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

    
=======

class VulnerabilityViewSet(ProjectRelatedObjectViewSet):
    queryset = models.Vulnerability.objects.all()
    serializer_class = serializers.VulnerabilitySerializer
>>>>>>> origin/dev
