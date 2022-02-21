from vulnman.api.viewsets import GenericListRetrieveModelViewSet, ProjectRelatedObjectViewSet
from apps.methodologies import models
from apps.methodologies.api.v1 import serializers


class TaskViewSet(GenericListRetrieveModelViewSet):
    # Only read information. Tasks are managed using YAML file imports
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    search_fields = ["name", "id", "description"]


class AssetTaskViewSet(ProjectRelatedObjectViewSet):
    queryset = models.AssetTask.objects.all()
    serializer_class = serializers.AssetTaskSerializer
