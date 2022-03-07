from rest_framework import serializers
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from vulnman.utils.markdown import md_to_clean_html
from apps.findings import models
from apps.assets.models import ASSET_TYPES_CHOICES, WebApplication, WebRequest, Host


class UserAccountSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.UserAccount
        fields = ["username", "password", "role", "account_compromised", "project"]


class TextProofSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.TextProof
        fields = ["order", "pk", "name", "description", "text"]


class ImageProofSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.ImageProof
        fields = ["pk", "order", "name", "description", "image", "caption"]


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Template
        fields = ["uuid", "vulnerability_id", "cwe_ids", "name", "description", "recommendation", "categories"]
        read_only_fields = ["uuid"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["description"] = md_to_clean_html(data["description"])
        return data

class VulnerabilitySerializer(ProjectRelatedObjectSerializer):
    # template = serializers.PrimaryKeyRelatedField(read_only=True)
    asset = serializers.CharField()

    def create(self, validated_data):
        asset_data = validated_data.pop('asset')
        if validated_data["asset_type"] == WebApplication.ASSET_TYPE:
            asset = WebApplication.objects.get(project=validated_data["project"], pk=asset_data)
            vulnerability = models.Vulnerability.objects.create(**validated_data, asset_webapp=asset)
        elif validated_data["asset_type"] == WebRequest.ASSET_TYPE:
            asset = WebRequest.objects.get(project=validated_data["project"], pk=asset_data)
            vulnerability = models.Vulnerability.objects.create(**validated_data, asset_webrequest=asset)
        return vulnerability

    class Meta:
        model = models.Vulnerability
        fields = ["name", "cve_id", "cvss_vector", "severity", "template", "asset", "status", "cvss_score", "project", "asset_type"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status"] = instance.get_status_display()
        return data
