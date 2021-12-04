from rest_framework import serializers
from apps.networking import models


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = "__all__"
        read_only_fields = ["creator", "uuid", "date_created", "date_updated"]
