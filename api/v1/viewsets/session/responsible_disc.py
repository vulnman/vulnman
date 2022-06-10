from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.responsible_disc import models
from api.v1.generics import ProjectSessionViewSet
from api.v1.serializers.responsible_disc import ImageProofSerializer, TextProofSerializer


class ProofViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    # Used to drag&drop reorder proofs in UI
    def get_queryset(self):
        if models.TextProof.objects.filter(pk=self.kwargs.get("pk"),
                                           vulnerability__user=self.request.user).exists():
            return models.TextProof.objects.filter(pk=self.kwargs.get("pk"))
        return models.ImageProof.objects.filter(pk=self.kwargs.get("pk"), vulnerability__user=self.request.user)

    def get_serializer_class(self):
        if models.TextProof.objects.filter(pk=self.kwargs.get("pk")).exists():
            return TextProofSerializer
        return ImageProofSerializer
