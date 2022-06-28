from django.conf import settings
from rest_framework import serializers
from django_celery_results.models import TaskResult
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.reporting import models


def get_report_templates():
    choices = []
    for template in settings.REPORT_TEMPLATES.keys():
        choices.append((template, template))
    return choices


class ReportSerializer(ProjectRelatedObjectSerializer):

    class Meta:
        model = models.PentestReport
        fields = ["uuid", "project", "report_type", "language"]
        read_only_fields = ["uuid"]


class PentestReportDraftCreateSerializer(ProjectRelatedObjectSerializer):
    report_template = serializers.ChoiceField(
        choices=get_report_templates(), required=False)

    class Meta:
        model = models.PentestReport
        fields = ["project", "report_type", "report_template"]


class PentestReportSerializer(ProjectRelatedObjectSerializer):
    report_template = serializers.ChoiceField(
        choices=get_report_templates())

    class Meta:
        model = models.PentestReport
        fields = ["project", "report_type", "name", "report_template", "language"]


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
