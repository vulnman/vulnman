from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter


class SessionModelViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    permission_classes = [IsAuthenticated]

    def get_project(self):
        if not self.request.session.get("project_pk"):
            raise PermissionDenied
        return self.request.session.get('project_pk')

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            project=self.get_project())

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.get_project()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(project=self.get_project())
