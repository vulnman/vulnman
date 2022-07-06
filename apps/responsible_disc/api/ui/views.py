from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.responsible_disc import models
from apps.responsible_disc.api.ui import serializers
from api.core import permission


class OrderProofViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    # Used to drag&drop reorder proofs in UI
    permission_classes = [IsAuthenticated, permission.ObjectPermission]

    def get_permission_object(self):
        proof = self.get_queryset().get()
        return proof.vulnerability

    def get_queryset(self):
        qs = models.TextProof.objects.filter(pk=self.kwargs.get("pk"))
        if qs.exists():
            return qs
        return models.ImageProof.objects.filter(pk=self.kwargs.get("pk"))

    def get_serializer_class(self):
        if models.TextProof.objects.filter(pk=self.kwargs.get("pk")).exists():
            return serializers.TextProofOrderSerializer
        return serializers.ImageProofOrderSerializer
