from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from apps.methodologies.models import Task
from apps.methodologies.api.ui import serializers


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    search_fields = ["name", "description"]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
