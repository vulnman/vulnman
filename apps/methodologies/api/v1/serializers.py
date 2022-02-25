from rest_framework import serializers
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from vulnman.utils.markdown import md_to_clean_html
from apps.methodologies import models
from apps.assets.api.v1.serializers import WebApplicationSerializer, HostSerializer, WebRequestSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ["task_id", "name", "description", "uuid"]
        read_only_fields = ["task_id", "name", "description", "uuid"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["description"] = md_to_clean_html(data["description"])
        return data


class AssetTaskSerializer(ProjectRelatedObjectSerializer):
    task = TaskSerializer()
    asset = serializers.SerializerMethodField()

    def get_asset(self, obj):
        if obj.asset.ASSET_TYPE == "webapplication":
            return WebApplicationSerializer(obj.asset).data
        elif obj.asset.ASSET_TYPE == "webrequest":
            return WebRequestSerializer(obj.asset).data
        elif obj.asset.ASSET_TYPE == "host":
            return HostSerializer(obj.asset).data
        return obj.asset

    class Meta:
        model = models.AssetTask
        fields = ["project", "task", "status", "asset"]
        read_only_fields = ["project", "task", "asset"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status"] = instance.get_status_display()
        return data
