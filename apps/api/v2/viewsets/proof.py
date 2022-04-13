from apps.api.v2 import generics
from apps.api import authentication
from apps.api.v2.serializers import proof as serializers
from apps.findings import models


class TextProofViewSet(generics.SearchModelViewSet):
    search_fields = ["name", "description", "text"]
    serializer_class = serializers.TextProofSerializer
    authentication_classes = [authentication.ProjectTokenAuthentication]

    def get_queryset(self):
        return models.TextProof.objects.filter(
            project=self.request.auth.project)

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            project=self.request.auth.project)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(self.request.auth.project, *args, **kwargs)
