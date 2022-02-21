from rest_framework import serializers
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.methodologies import models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ["task_id", "name", "description"]
        read_only_fields = ["task_id", "name", "description"]


class AssetTaskSerializer(ProjectRelatedObjectSerializer):

    class Meta:
        model = models.AssetTask
        fields = ["project", "task", "status"]
