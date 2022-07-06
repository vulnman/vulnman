from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from django_celery_results.models import TaskResult
from vulnman.api import viewsets
from apps.reporting import models
from api.v1.serializers import reports as serializers


class ReportTaskResultViewSet(RetrieveModelMixin, GenericViewSet):
    # TODO: make this more generic.
    # TODO: legacy
    # do not use this one just for report tasks but all tasks
    queryset = TaskResult.objects.all()
    serializer_class = serializers.ReportTaskSerializer
    lookup_field = "task_id"


class ReportViewSet(viewsets.ProjectRelatedDontDestroyObjectViewSet):
    # TODO: legacy
    queryset = models.Report
    serializer_class = serializers.ReportSerializer
