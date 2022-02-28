from rest_framework import serializers
from apps.methodologies import models


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = models.Task
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_updated", "date_created", "methodology"]


class MethodologySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, source='task_set')
    creator = serializers.StringRelatedField()

    class Meta:
        model = models.Methodology
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_updated", "date_created"]

    def create(self, validated_data):
        if validated_data.get('task_set'):
            tasks_validated_data = validated_data.pop('task_set')
            methodology = models.Methodology.objects.create(**validated_data)
            tasks_serializer = self.fields["tasks"]
            for task in tasks_validated_data:
                task["methodology"] = methodology
                task["creator"] = methodology.creator
            tasks_serializer.create(tasks_validated_data)
        else:
            methodology = models.Methodology.objects.create(**validated_data)
        return methodology


class ProjectTaskStatusUpdateSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = models.ProjectTask
        fields = ["status", "creator"]
        read_only_fields = ["creator"]
