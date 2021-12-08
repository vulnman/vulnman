from rest_framework import serializers
from apps.networking import models


class HostnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hostname
        fields = ["name"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ["uuid", "name", "protocol", "port"]
        read_only_fields = ["uuid"]


class HostSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    hostnames = HostnameSerializer(source="hostname_set", many=True, read_only=True)
    services = ServiceSerializer(source="service_set", many=True, read_only=True)

    class Meta:
        model = models.Host
        fields = "__all__"
        read_only_fields = ["creator", "uuid", "date_created", "date_updated"]
