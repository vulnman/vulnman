from vulnman.api.viewsets import VulnmanModelViewSet
from django.utils.module_loading import import_string
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from dry_rest_permissions.generics import DRYPermissions
from django.conf import settings
from apps.commands import models
from apps.commands.api.v1 import serializers


class CommandTemplateViewSet(VulnmanModelViewSet):
    search_fields = ["command", "tool_name", "name"]
    serializer_class = serializers.CommandTemplateSerializer
    queryset = models.CommandTemplate.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CommandHistoryViewSet(VulnmanModelViewSet):
    search_fields = ["command", "output"]
    serializer_class = serializers.CommandHistoryItemSerializer
    ignore_fields_after_creation = ["project"]

    def get_queryset(self):
        return models.CommandHistoryItem.objects.filter(project__creator=self.request.user)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated, DRYPermissions],
            authentication_classes=[SessionAuthentication])
    def push(self, request, pk=None):
        serializer = serializers.CommandHistoryPushSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.validated_data["project"]
            if not project.creator == self.request.user:
                return Response({"project": "invalid project"}, status=status.HTTP_403_FORBIDDEN)
            new_instance = serializer.save(creator=self.request.user, project=project)
            self._parse_results(new_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _parse_results(self, instance):
        plugin_exists = False
        for plugin_name, cls in settings.EXTERNAL_TOOLS.items():
            plugin_module = import_string(settings.EXTERNAL_TOOLS[plugin_name])
            plugin = plugin_module()
            if instance.command.startswith(plugin.get_tool_name()):
                plugin_exists = True
                if instance.agent:
                    plugin.parse(instance.output, instance.project, instance.agent.user, command=instance)
                else:
                    plugin.parse(instance.output, instance.project, instance.creator, command=instance)
                break
        if plugin_exists:
            print("Plugin found")
