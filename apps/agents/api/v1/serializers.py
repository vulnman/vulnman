from rest_framework import serializers
from apps.agents import models


class AgentQueueSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = models.AgentQueue
        fields = '__all__'
        read_only_fields = ["creator", "uuid", "date_created", "date_updated"]
