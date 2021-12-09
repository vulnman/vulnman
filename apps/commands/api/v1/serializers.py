from rest_framework import serializers
from apps.commands import models


class CommandTemplateSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = models.CommandTemplate
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_created", "date_updated"]


class CommandHistoryItemSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = models.CommandHistoryItem
        fields = '__all__'
        read_only_fields = ["creator", "uuid", "project", "agent", "date_created", "date_updated"]
