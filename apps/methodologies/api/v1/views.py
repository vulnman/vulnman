from vulnman.api.viewsets import VulnmanModelViewSet
from apps.methodologies import models
from apps.methodologies.api.v1 import serializers


class MethodologyViewSet(VulnmanModelViewSet):
    search_fields = ["name", "task__name", "task__description"]
    queryset = models.Methodology.objects.all()
    serializer_class = serializers.MethodologySerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
