from rest_framework import serializers
from apps.assets import models


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = [
            "uuid", "ip", "operating_system", "accessibility",
            "description", "dns", "project"]
        read_only_fields = ["uuid", "project"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["name"] = str(instance)
        return data

    def create(self, validated_data):
        # prevent duplicate entries here and just return existing ones
        qs = models.Host.objects.filter(
            project=validated_data["project"], ip=validated_data["ip"])
        if qs.exists():
            return qs.get()
        return super().create(validated_data)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = [
            "uuid", "name", "port", "host", "protocol", "state",
            "banner", "project"]
        read_only_fields = ["uuid", "project"]

    def create(self, validated_data):
        qs = models.Service.objects.filter(
            project=validated_data["project"],
            host=validated_data["host"],
            port=validated_data["port"],
            protocol=validated_data["protocol"]
        )
        if qs.exists():
            return qs.get()
        return super().create(validated_data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["host"].queryset = self.context.get(
            'project').host_set.all()
