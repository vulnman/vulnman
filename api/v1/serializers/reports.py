from rest_framework import serializers
from django_celery_results.models import TaskResult
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.reporting import models


class ReportSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.PentestReport
        fields = ["uuid", "project", "report_type"]
        read_only_fields = ["uuid"]


class PentestReportDraftCreateSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.PentestReport
        fields = ["project", "report_type"]


class PentestReportSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.PentestReport
        fields = ["project", "report_type", "name"]


class PentestReportInformationSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.ReportInformation
        fields = ["evaluation", "recommendation", "project", "uuid", "author"]
        read_only_fields = ["uuid", "project"]


class ReportTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ["status", "task_id", "result"]
        read_only_fields = ["status", "task_id", "result"]
