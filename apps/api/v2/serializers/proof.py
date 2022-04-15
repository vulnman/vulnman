from rest_framework import serializers
from apps.findings import models


class TextProofSerializer(serializers.ModelSerializer):
    # TODO: filter vulnerability FK on update/create
    class Meta:
        model = models.TextProof
        fields = [
            "order", "pk", "name", "description", "text",
            "project", "vulnerability"]
        read_only_fields = ["pk", "project"]

    def create(self, validated_data):
        qs = models.TextProof.objects.filter(
            project=validated_data["project"],
            vulnerability=validated_data["vulnerability"],
            name=validated_data["name"])
        if qs.exists():
            return qs.get()
        return super().create(validated_data)
