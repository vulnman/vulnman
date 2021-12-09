from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import mixins
from apps.agents.api import serializers
from apps.agents import models
from apps.agents.api.authentication import AgentAuthentication
from apps.projects.models import CommandHistoryItem



class CommandHistoryItemViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CommandHistoryItemSerializer
    authentication_classes = [AgentAuthentication]

    def get_queryset(self):
        return CommandHistoryItem.objects.filter(agent=self.request.auth)

    def perform_update(self, serializer):
        instance = serializer.save()
        plugin_exists = False
        for plugin_name, cls in settings.EXTERNAL_TOOLS.items():
            plugin_module = import_string(settings.EXTERNAL_TOOLS[plugin_name])
            plugin = plugin_module()
            if instance.command.startswith(plugin.get_tool_name()):
                plugin_exists = True
                plugin.parse(instance.output, instance.project, instance.agent.user)
                break
        if plugin_exists:
            print("Plugin found")
