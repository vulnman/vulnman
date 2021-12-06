from rest_framework import serializers
from apps.methodologies import models


class SuggestedCommandSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = models.SuggestedCommand
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_updated", "date_created"]


class MethodologySerializer(serializers.ModelSerializer):
    commands = SuggestedCommandSerializer(many=True, source='suggestedcommand_set')
    creator = serializers.StringRelatedField()

    class Meta:
        model = models.Methodology
        fields = '__all__'
        read_only_fields = ["uuid", "creator", "date_updated", "date_created"]
