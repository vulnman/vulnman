from rest_framework import serializers
from apps.projects import models


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = ["uuid", "name", "start_date", "end_date", "client"]
        read_only_fields = ["uuid"]
