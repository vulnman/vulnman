from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.assets import models


class WebApplicationSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.WebApplication
        fields = ["uuid", "name", "base_url", "description", "project"]
        read_only_fields = ["uuid"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["asset_type"] = models.WebApplication.ASSET_TYPE_CHOICE[1]
        data["display_name"] = instance.name
        return data


class WebRequestSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.WebRequest
        fields = ["name", "description", "web_app", "url", "parameter"]

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
