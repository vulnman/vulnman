from rest_framework import serializers
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.findings import models

"""
class VulnerabilitySerializer(serializers.ModelSerializer):
    template = TemplateSerializer()

    class Meta:
        model = models.Vulnerability
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_updated", "date_created", "command_created"]

    def create(self, validated_data):
        if validated_data.get('vulnerabilitydetails'):
            detail_validated_data = validated_data.pop('vulnerabilitydetails')
            vulnerability = models.Vulnerability.objects.create(**validated_data)
            detail_serializer = self.fields["details"]
            detail_validated_data["project"] = vulnerability.project
            detail_validated_data["creator"] = vulnerability.creator
            detail_validated_data["vulnerability"] = vulnerability
            detail_serializer.create(detail_validated_data)
        else:
            vulnerability = models.Vulnerability.objects.create(**validated_data)
        return vulnerability
"""

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
        fields = ["pk", "order", "name", "description", "image"]


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Template
        fields = ["uuid", "vulnerability_id", "cwe_ids", "name", "description", "recommendation", "categories"]
        read_only_fields = ["uuid"]


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
        fields = ["name", "cve_id", "cvss_vector", "severity", "template", "asset", "verified", "is_fixed", 
                "false_positive", "cvss_score", "project"]
