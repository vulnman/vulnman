from vulnman.api import viewsets
from apps.social.api.v1 import serializers
from apps.social import models


class CredentialViewSet(viewsets.VulnmanModelViewSet):
    serializer_class = serializers.CredentialSerializer
    search_fields = ["username", "cleartext_password", "hashed_password", "description"]
    ignore_fields_after_creation = ["project"]

    def get_queryset(self):
        return models.Credential.objects.filter(project__creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
