from rest_framework import serializers
from apps.social import models


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Credential
        fields = '__all__'
        read_only_fields = ["uuid", "date_created", "date_updated", "creator", "command_created"]
