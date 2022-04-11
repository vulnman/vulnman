from apps.api.v2 import generics
from apps.assets import models
from apps.api.v2.serializers import assets as serializers
from apps.api import authentication


class ServiceViewSet(generics.SearchModelViewSet):
    search_fields = ["name"]
    serializer_class = serializers.ServiceSerializer
    authentication_classes = [authentication.ProjectTokenAuthentication]

    def get_queryset(self):
        return models.Service.objects.filter(project=self.request.auth.project)

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            project=self.request.auth.project)


class HostViewSet(generics.SearchModelViewSet):
    search_fields = ["ip", "dns"]
    serializer_class = serializers.HostSerializer
    authentication_classes = [authentication.ProjectTokenAuthentication]

    def get_queryset(self):
        return models.Host.objects.filter(project=self.request.auth.project)

    def perform_create(self, serializer):
        serializer.save(
            project=self.request.auth.project,
            creator=self.request.user
        )
