from rest_framework import serializers
from apps.findings import models


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Template
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_updated", "date_created"]
