from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.findings import models


class TextProofSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.TextProof
        fields = [
            "order", "pk", "name", "description", "text",
            "project", "vulnerability"]
        read_only_fields = ["pk"]


class ImageProofSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.ImageProof
        fields = [
            "pk", "order", "name", "description", "image",
            "caption"]
