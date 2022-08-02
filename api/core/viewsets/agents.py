from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from api.core import mixins
from api.core import authentication


class AgentModelViewSet(mixins.AgentCreateModelMixin, mixins.AgentRetrieveModelMixin, mixins.AgentUpdateModelMixin,
                        mixins.AgentDestroyModelMixin, mixins.AgentListModelMixin, viewsets.GenericViewSet):
    filter_backends = [SearchFilter]
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.request.auth.project
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(project=self.request.auth.project)
