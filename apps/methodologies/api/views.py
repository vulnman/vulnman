from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from apps.methodologies import models
from apps.methodologies.api import serializers


class MethodologyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "suggestedcommand__name", "suggestedcommand__command"]
    queryset = models.Methodology.objects.all()
    serializer_class = serializers.MethodologySerializer
