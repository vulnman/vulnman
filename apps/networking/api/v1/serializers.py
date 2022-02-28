from rest_framework import serializers
from apps.networking import models


class HostnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hostname
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_updated", "date_created", "command_created"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_updated", "date_created", "command_created"]


class HostSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    hostnames = HostnameSerializer(source="hostname_set", many=True, read_only=True)
    services = ServiceSerializer(source="service_set", many=True, read_only=True)

    class Meta:
        model = models.Host
        fields = "__all__"
        read_only_fields = ["creator", "uuid", "date_created", "date_updated", "command_created"]
