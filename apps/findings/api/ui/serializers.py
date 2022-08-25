from rest_framework import serializers
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.findings import models


class TemplateSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Template
        fields = ["uuid", "vulnerability_id", "name", "url"]
        read_only_fields = ["uuid", "vulnerability_id", "name", "url"]

    def get_url(self, obj):
        return obj.get_absolute_url()


class TextProofSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.TextProof
        fields = ["order", "pk", "name", "description", "text", "project", "vulnerability"]
        read_only_fields = ["pk"]


class ImageProofSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.ImageProof
        fields = ["pk", "order", "name", "description", "image", "caption"]
