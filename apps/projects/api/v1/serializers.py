from django.contrib.auth.models import User
from rest_framework import serializers
from apps.projects import models
from vulnman.api.serializers import AssignObjectPermissionsModelSerializer
from vulnman.api.serializers import ProjectRelatedObjectSerializer
from apps.assets.api.v1.serializers import WebApplicationSerializer, WebRequestSerializer, HostSerializer


class ClientSerializer(ProjectRelatedObjectSerializer):
    class Meta:
        model = models.Client
        fields = ["uuid", "name"]
        read_onyl_fields = ["uuid"]


class ProjectSerializer(AssignObjectPermissionsModelSerializer):
    vulnerabilities = serializers.PrimaryKeyRelatedField(source="vulnerability_set", read_only=True, many=True)
    user_accounts = serializers.PrimaryKeyRelatedField(source="useraccount_set", read_only=True, many=True)
    tasks = serializers.PrimaryKeyRelatedField(source="assettask_set", read_only=True, many=True)
    contributors = serializers.PrimaryKeyRelatedField(source="projectcontributor_set", read_only=True, many=True)
    assets_webapplication = WebApplicationSerializer(source="webapplication_set", read_only=True, many=True)
    assets_webrequest = WebRequestSerializer(source="webrequest_set", many=True, read_only=True)
    assets_host = HostSerializer(source="host_set", many=True, read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = models.Project
        fields = ["uuid", "name", "start_date", "end_date", "client", "vulnerabilities", 
            "user_accounts", "tasks", "contributors", "assets_webapplication",
            "assets_webrequest", "assets_host"]
        read_only_fields = ["uuid"]

    def get_permissions_map(self, created):
        current_user = self.context["request"].user
        return {
            "view_project": [current_user],
            "change_project": [current_user],
            "delete_project": [current_user]
        }


class ProjectContributorSerializer(ProjectRelatedObjectSerializer):
    user = serializers.CharField()

    def validate_user(self, data):
        if not User.objects.filter(username=data).exists():
            raise serializers.ValidationError("Invalid user")
        return data

    class Meta:
        model = models.ProjectContributor
        fields = ["role", "user", "project"]

    def create(self, validated_data):
        validated_data["user"] = User.objects.get(username=validated_data["user"])
        return super().create(validated_data)


class ProjectArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["is_archived"]

