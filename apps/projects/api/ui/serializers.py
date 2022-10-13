from django.db.models import Count
from rest_framework import serializers
from apps.projects import models
from apps.findings.models import Vulnerability, SEVERITY_CHOICES, VulnerabilityCategory


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = ["uuid", "name", "start_date", "end_date"]
        read_only_fields = ["uuid"]


class StatsVulnsBySeveritySerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField()
    severities = serializers.SerializerMethodField()

    def get_colors(self, _obj):
        return [
            Vulnerability.SEVERITY_COLOR_CRITICAL,
            Vulnerability.SEVERITY_COLOR_HIGH,
            Vulnerability.SEVERITY_COLOR_MEDIUM,
            Vulnerability.SEVERITY_COLOR_LOW,
            Vulnerability.SEVERITY_COLOR_INFORMATIONAL
        ]

    def get_severities(self, obj):
        severities = []
        for severity in SEVERITY_CHOICES:
            severities.append(obj.vulnerability_set.filter(
                severity=severity[0]).count())
        return severities

    class Meta:
        model = models.Project
        fields = ["colors", "severities"]


class StatsHostsByServicesSerializer(serializers.ModelSerializer):
    ips = serializers.SerializerMethodField()
    counts = serializers.SerializerMethodField()

    def get_ips(self, obj):
        return obj.host_set.annotate(count=Count(
            'service__pk')).values("count").order_by(
                "-count").values_list("ip", flat=True)[:5]

    def get_counts(self, obj):
        return obj.host_set.annotate(count=Count(
            'service__pk')).values("count").order_by(
                "-count").values_list("count", flat=True)[:5]

    class Meta:
        model = models.Project
        fields = ["ips", "counts"]
