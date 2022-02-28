from rest_framework import serializers
<<<<<<< HEAD
from apps.findings import models


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Template
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_updated", "date_created"]


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
=======
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from vulnman.utils.markdown import md_to_clean_html
from apps.assets import models


class WebApplicationSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.WebApplication
        fields = ["uuid", "name", "base_url", "description", "in_pentest_report"]
        read_only_fields = ["uuid"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["asset_type"] = models.WebApplication.ASSET_TYPE_CHOICE[1]
        return data


class WebRequestSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.WebRequest
        fields = ["name", "description", "in_pentest_report", "web_app", "url", "parameter"]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["asset_type"] = models.WebRequest.ASSET_TYPE_CHOICE[1]
        return data


class HostSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.Host
        fields = ["ip", "operating_system", "accessibility", "description", "dns"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["asset_type"] = models.Host.ASSET_TYPE_CHOICE[1]
        return data
>>>>>>> origin/dev
