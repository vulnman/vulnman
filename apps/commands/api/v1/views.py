from vulnman.api.viewsets import VulnmanModelViewSet
from apps.commands import models
from apps.commands.api.v1 import serializers


class CommandTemplateViewSet(VulnmanModelViewSet):
    search_fields = ["command", "tool_name", "name"]
    serializer_class = serializers.CommandTemplateSerializer
    queryset = models.CommandTemplate.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
