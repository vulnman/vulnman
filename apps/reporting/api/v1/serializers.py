from rest_framework import serializers
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.reporting import models


class ReportSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.PentestReport
        fields = ["uuid", "project", "author", "report_type"]
        read_only_fields = ["uuid"]


class PentestReportCreateSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.PentestReport
        fields = ["project", "report_type"]


class PentestReportInformationSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.ReportInformation
        fields = ["evaluation", "recommendation", "project", "uuid", "author"]
        read_only_fields = ["uuid", "project"]
