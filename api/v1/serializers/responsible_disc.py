from rest_framework import serializers
from apps.responsible_disc import models


class TextProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TextProof
        fields = [
            "order", "pk", "name", "description", "text", "vulnerability"]
        read_only_fields = ["pk"]


class ImageProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageProof
        fields = [
            "pk", "order", "name", "description", "image", "caption"]
        read_only_fields = ["pk"]
