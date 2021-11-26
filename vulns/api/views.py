from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from vulns.api import serializers
from vulns import models


class VulnerabilityTemplateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.VulnerabilityTemplateSerializer
    queryset = models.VulnerabilityTemplate
