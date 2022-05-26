from rest_framework import serializers
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.assets import models


class AgentHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = [
            "uuid", "ip", "operating_system", "accessibility",
            "description", "dns", "project"]
        read_only_fields = ["uuid", "project"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["asset_type"] = models.Host.ASSET_TYPE_CHOICE[1]
        data["name"] = str(instance)
        return data

    def create(self, validated_data):
        qs = models.Host.objects.filter(
            project=validated_data["project"], ip=validated_data["ip"])
        if qs.exists():
            return qs.get()
        return super().create(validated_data)


class AgentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = [
            "uuid", "name", "port", "host", "protocol", "state",
            "banner", "project"]
        read_only_fields = ["uuid", "project"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["asset_type"] = models.Service.ASSET_TYPE_CHOICE[1]
        return data

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
        if self.instance is not None:
            self.fields["host"].read_only = True

# Legacy Serializers
class WebApplicationSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.WebApplication
        fields = ["uuid", "name", "base_url", "description", "in_pentest_report", "project"]
        read_only_fields = ["uuid"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["asset_type"] = models.WebApplication.ASSET_TYPE_CHOICE[1]
        data["display_name"] = instance.name
        return data


class WebRequestSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.WebRequest
        fields = ["name", "description", "in_pentest_report", "web_app", "url", "parameter"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["asset_type"] = models.WebRequest.ASSET_TYPE_CHOICE[1]
        data["display_name"] = instance.name
        return data


class HostSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.Host
        fields = ["uuid", "ip", "operating_system", "accessibility", "description", "dns", "project"]
        read_only_fields = ["uuid"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["asset_type"] = models.Host.ASSET_TYPE_CHOICE[1]
        data["name"] = str(instance)
        data["display_name"] = str(instance)
        return data


class ServiceSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.Service
        fields = ["uuid", "name", "port", "host", "protocol", "state", "banner", "project"]
        read_only_fields = ["uuid"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["asset_type"] = models.Service.ASSET_TYPE_CHOICE[1]
        data["display_name"] = "%s:%s (%s)" % (instance.host.ip, instance.port, instance.name)
        return data
