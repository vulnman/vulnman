from rest_framework import serializers
from apps.projects import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["name", "customer", "report_default_title", "start_date", "end_date"]
