from rest_framework import serializers
from django_q.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["success", "started"]
        read_only_fields = ["success", "started"]
        ref_name = "ReportTaskSerializer"
