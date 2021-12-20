from rest_framework import serializers
from apps.projects import models


class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    client = serializers.StringRelatedField()
    vulnerabilities = serializers.PrimaryKeyRelatedField(source="vulnerability_set", read_only=True, many=True)
    hosts = serializers.PrimaryKeyRelatedField(source="host_set", read_only=True, many=True)
    services = serializers.PrimaryKeyRelatedField(source="service_set", read_only=True, many=True)

    class Meta:
        model = models.Project
        fields = '__all__'
        read_only_fields = ["uuid", "creator"]
