from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from api.v1 import authentication


class AgentModelViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.AgentTokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            project=self.request.auth.project)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.request.auth.project
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(project=self.request.auth.project)
