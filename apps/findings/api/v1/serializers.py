from rest_framework import serializers
from apps.findings import models


class VulnerabilitySerializer(serializers.ModelSerializer):
    template_id = serializers.CharField()
    asset = serializers.UUIDField()

    def validate_asset(self, value):
        Asset = models.Vulnerability.objects.get_asset_model_cls(value)
        project = self.context.get('project')
        if not Asset.objects.filter(project=project, pk=value).exists():
            raise serializers.ValidationError("Invalid asset")
        return value

    def check_exists(self, validated_data):
        template = models.Template.objects.filter(
            vulnerability_id=validated_data["template_id"])
        if not template.exists():
            return
        template = template.get()
        qs = models.Vulnerability.objects.filter(
            name=validated_data["name"],
            project=self.context["project"],
            template=template, content_type=models.Vulnerability.objects.get_asset_content_type(
                validated_data["asset"]), object_id=validated_data["asset"]
        )
        if qs.exists():
            return qs.get()
        return

    def create(self, validated_data):
        qs = self.check_exists(validated_data)
        if qs:
            return qs
        validated_data["object_id"] = validated_data["asset"]
        validated_data["content_type"] = models.Vulnerability.objects.get_asset_content_type(validated_data["asset"])
        validated_data.pop("asset")
        return super().create(validated_data)

    class Meta:
        model = models.Vulnerability
        fields = [
            "name", "cve_id", "severity", "template_id", "asset",
            "status", "project", "uuid"]
        read_only_fields = ["uuid", "project"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status"] = instance.get_status_display()
        data["template_id"] = instance.template.vulnerability_id
        return data


class TextProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TextProof
        fields = [
            "order", "uuid", "name", "description", "text",
            "project", "vulnerability"]
        read_only_fields = ["uuid", "project"]

    def create(self, validated_data):
        qs = models.TextProof.objects.filter(
            vulnerability__project=self.context["project"],
            vulnerability=validated_data["vulnerability"],
            name=validated_data["name"])
        if qs.exists():
            return qs.get()
        return super().create(validated_data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project = self.context["project"]
        self.fields["vulnerability"].queryset = project.vulnerability_set.all()
