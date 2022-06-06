from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from api.v1 import mixins
from api.v1.permissions import ProjectPermission


class ProjectSessionViewSet(mixins.ProjectSessionAPIMixin, mixins.ProjectPermissionRequiredMixin,
                            viewsets.GenericViewSet):
    """
    A viewset for session based authenticated users.
    Check permissions of the user to the project.
    """
    permission_classes = [IsAuthenticated, ProjectPermission]
    filter_backends = [SearchFilter]
