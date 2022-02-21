from rest_framework import serializers
from apps.projects import models
from vulnman.api.serializers import AssignObjectPermissionsModelSerializer


class ProjectSerializer(AssignObjectPermissionsModelSerializer):
    vulnerabilities = serializers.PrimaryKeyRelatedField(source="vulnerability_set", read_only=True, many=True)
    user_accounts = serializers.PrimaryKeyRelatedField(source="useraccount_set", read_only=True, many=True)
    tasks = serializers.PrimaryKeyRelatedField(source="assettask_set", read_only=True, many=True)

    class Meta:
        model = models.Project
        fields = ["uuid", "name", "start_date", "end_date", "client", "vulnerabilities", 
            "user_accounts", "tasks"]
        read_only_fields = ["uuid"]

    def get_permissions_map(self, created):
        current_user = self.context["request"].user
        return {
            "view_project": [current_user],
            "change_project": [current_user],
            "delete_project": [current_user]
        }
