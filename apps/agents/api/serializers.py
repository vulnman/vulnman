from rest_framework import serializers
from apps.agents import models
from apps.projects.models import CommandHistoryItem


class AgentQueueSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = models.AgentQueue
        fields = '__all__'
        read_only_fields = ["creator", "uuid", "project", "date_created", "date_updated"]


class CommandHistoryItemSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = CommandHistoryItem
        fields = '__all__'
        read_only_fields = ["creator", "uuid", "project", "agent", "date_created", "date_updated"]
