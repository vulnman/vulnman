from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from apps.findings import models
from apps.findings.api.ui import serializers
from api.v1.generics import ProjectSessionViewSet


class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: write tests
    queryset = models.Template.objects.all()
    serializer_class = serializers.TemplateSerializer
    search_fields = ["name", "vulnerability_id", "description"]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]


class ProofViewSet(mixins.UpdateModelMixin, ProjectSessionViewSet):
    # Used to drag&drop reorder proofs in UI
    # TODO: write Tests
    def get_queryset(self):
        if models.TextProof.objects.filter(pk=self.kwargs.get("pk"),
                                           vulnerability__project=self.get_project()).exists():
            return models.TextProof.objects.filter(pk=self.kwargs.get("pk"))
        return models.ImageProof.objects.filter(pk=self.kwargs.get("pk"), vulnerability__project=self.get_project())

    def get_serializer_class(self):
        if models.TextProof.objects.filter(pk=self.kwargs.get("pk")).exists():
            return serializers.TextProofSerializer
        return serializers.ImageProofSerializer
