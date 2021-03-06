from django.conf import settings
from rest_framework import serializers
#from django_celery_results.models import TaskResult
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.reporting import models


def get_report_templates():
    choices = []
    for template in settings.REPORT_TEMPLATES.keys():
        choices.append((template, template))
    return choices


class ReportSerializer(ProjectRelatedObjectSerializer):

    class Meta:
        model = models.Report
        fields = ["uuid", "evaluation", "recommendation"]
        read_only_fields = ["uuid"]


class PentestReportInformationSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.Report
        fields = ["evaluation", "recommendation", "project", "uuid", "author"]
        read_only_fields = ["uuid", "project"]


class ReportTaskSerializer(serializers.ModelSerializer):
    class Meta:
        #model = TaskResult
        fields = ["status", "task_id", "result"]
        read_only_fields = ["status", "task_id", "result"]
