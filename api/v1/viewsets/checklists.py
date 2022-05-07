from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from core import models
from api.v1.serializers import checklists as serializers


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    search_fields = ["name", "description"]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
