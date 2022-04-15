from vulnman.api.viewsets import ProjectRelatedObjectViewSet, GenericListRetrieveModelViewSet, ProjectRelatedObjectCreateViewSet
from apps.findings import models
from apps.findings.api.v1 import serializers


class UserAccountViewSet(ProjectRelatedObjectViewSet):
    queryset = models.UserAccount.objects.all()
    serializer_class = serializers.UserAccountSerializer


class TextProofViewSet(ProjectRelatedObjectCreateViewSet):
    queryset = models.TextProof.objects.all()
    serializer_class = serializers.TextProofSerializer


class VulnerabilityViewSet(ProjectRelatedObjectViewSet):
    queryset = models.Vulnerability.objects.all()
    serializer_class = serializers.VulnerabilitySerializer
