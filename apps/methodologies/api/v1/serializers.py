from rest_framework import serializers
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from vulnman.utils.markdown import md_to_clean_html
from apps.methodologies import models


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

    class Meta:
        model = models.AssetTask
        fields = ["project", "task", "status"]
