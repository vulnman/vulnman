from django.utils import timezone
from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import mixins
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from dry_rest_permissions.generics import DRYPermissions
from vulnman.api.mixins import IgnoreFieldsAfterCreationMixin
from apps.agents.api.v1 import serializers
from apps.agents.api.authentication import AgentAuthentication
from apps.agents import models


class AgentQueueViewSet(IgnoreFieldsAfterCreationMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = serializers.AgentQueueSerializer
    authentication_classes = [AgentAuthentication]
    ignore_fields_after_creation = ["project", "command"]

    def get_queryset(self):
        if self.action == "list":
            return models.AgentQueue.objects.filter(project__creator=self.request.user, in_progress=False,
                                                    exit_code__isnull=True)
        return models.AgentQueue.objects.filter(project__creator=self.request.user, exit_code__isnull=True)

    def perform_update(self, serializer):
        # queue item is in progress
        if serializer.validated_data.get('in_progress'):
            serializer.save(agent=self.request.auth, execution_started=timezone.now())
        # queue item execution finished
        if serializer.validated_data.get('exit_code') is not None:
            instance = serializer.save(execution_ended=timezone.now(), in_progress=False)
            self._parse_results(instance)
        # do not save here because the data is invalid

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated, DRYPermissions],
            authentication_classes=[SessionAuthentication])
    def push(self, request, pk=None):
        """
        *real* users are allowed to queue new commands

        :param request:
        :param pk:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _parse_results(self, instance):
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
