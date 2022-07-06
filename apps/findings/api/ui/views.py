from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from apps.findings import models
from apps.findings.api.ui import serializers


class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: write tests
    queryset = models.Template.objects.all()
    serializer_class = serializers.TemplateSerializer
    search_fields = ["name", "vulnerability_id", "description"]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
