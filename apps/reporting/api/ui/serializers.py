from rest_framework import serializers
from django_celery_results.models import TaskResult


class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ["status", "task_id", "result"]
        read_only_fields = ["status", "task_id", "result"]
