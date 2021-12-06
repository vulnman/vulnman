from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from vulnman.api.permission import HasProjectPermission
from apps.networking import models
from apps.networking.api import serializers


class HostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HostSerializer
    permission_classes = [HasProjectPermission, IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["ip", "hostname__name"]

    def get_queryset(self):
        return models.Host.objects.filter(project__creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
