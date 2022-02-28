from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username"]
        read_only_fields = ["username"]
