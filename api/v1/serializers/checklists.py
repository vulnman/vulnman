from rest_framework import serializers
from vulnman.utils.markdown import md_to_clean_html
from apps.methodologies import models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = [
            "uuid", "name", "description", "task_id"]
        read_only_fields = ["uuid"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["description"] = md_to_clean_html(data["description"])
        return data
