from rest_framework import serializers
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from vulnman.utils.markdown import md_to_clean_html
from apps.findings import models


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
    asset = serializers.SerializerMethodField()

    def get_asset(self, obj):
        asset = obj.asset
        if asset:
            return {
                "uuid": str(asset.pk), "type": asset._meta.verbose_name,
                "name": asset.name
            }
        return {"uuid": None}

    class Meta:
        model = models.Vulnerability
        fields = ["name", "cve_id", "cvss_vector", "severity", "template", "asset", "status", "cvss_score", "project"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status"] = instance.get_status_display()
        return data
