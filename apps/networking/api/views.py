from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from vulnman.api.permissions import HasProjectPermission
from apps.networking import models
from apps.networking.api import serializers


class HostViewSet(viewsets.ModelViewSet):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer
    permission_classes = [HasProjectPermission, IsAuthenticated]

    def get_queryset(self):
        return models.Host.objects.filter(project__creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
