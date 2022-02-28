from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from vulnman.api.viewsets import VulnmanModelViewSet
from apps.methodologies import models
from apps.methodologies.api.v1 import serializers


class MethodologyViewSet(VulnmanModelViewSet):
    search_fields = ["name", "task__name", "task__description"]
    queryset = models.Methodology.objects.all()
    serializer_class = serializers.MethodologySerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ProjectTaskViewSet(VulnmanModelViewSet):
    search_fields = ["name", "description"]
    serializer_class = serializers.ProjectTaskStatusUpdateSerializer

    def get_queryset(self):
        return models.ProjectTask.objects.filter(project__creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=["patch"])
    def status(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
