from rest_framework import serializers
from apps.findings import models


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Template
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_updated", "date_created"]


class VulnerabilityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VulnerabilityDetails
        exclude = ["template", "project", "vulnerability"]
        read_only_fields = ["uuid", "creator", "date_updated", "date_created"]


class VulnerabilitySerializer(serializers.ModelSerializer):
    details = VulnerabilityDetailSerializer(source='vulnerabilitydetails')

    class Meta:
        model = models.Vulnerability
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_updated", "date_created"]

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
