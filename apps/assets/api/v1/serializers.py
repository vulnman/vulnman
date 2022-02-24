from rest_framework import serializers
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from vulnman.utils.markdown import md_to_clean_html
from apps.assets import models


class WebApplicationSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.WebApplication
        fields = ["uuid", "name", "base_url", "description", "in_pentest_report"]
        read_only_fields = ["uuid"]


class WebRequestSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.WebRequest
        fields = ["name", "description", "in_pentest_report", "web_app", "url", "parameter"]


class HostSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.Host
        fields = ["ip", "operating_system", "accessibility", "description", "dns"]