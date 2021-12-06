from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from apps.findings.api import serializers
from apps.findings import models


class TemplateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TemplateSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "description", "remediation"]
    queryset = models.Template.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
