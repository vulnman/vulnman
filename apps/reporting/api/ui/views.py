from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from django_celery_results.models import TaskResult
from apps.reporting.api.ui import serializers


class TaskResultViewSet(RetrieveModelMixin, GenericViewSet):
    # TODO: Write Tests
    queryset = TaskResult.objects.all()
    serializer_class = serializers.TaskResultSerializer
    lookup_field = "task_id"
