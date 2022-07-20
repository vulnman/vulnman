from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from django_q.models import Task
from apps.reporting.api.ui import serializers


class TaskResultViewSet(RetrieveModelMixin, GenericViewSet):
#    # TODO: Write Tests
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        return Task.objects.all()
