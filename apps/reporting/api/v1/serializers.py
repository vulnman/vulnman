from rest_framework import serializers
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.reporting import models


class ReportStatusSerializer(serializers.Serializer):
    task = serializers.CharField()

    class Meta:
        fields = ["task"]
