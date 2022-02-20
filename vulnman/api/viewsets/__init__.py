from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from vulnman.api.permissions import BaseObjectPermission, ProjectRelatedObjectPermission
from vulnman.api import filters


class VulnmanModelViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [BaseObjectPermission, IsAuthenticated]
    filter_backends = [SearchFilter]
    # filter_backends = [filters.ObjectPermissionsFilter]


class ProjectRelatedObjectViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ProjectRelatedObjectPermission]
    filter_backends = [SearchFilter]


class GenericListRetrieveModelViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    filter_backends = [SearchFilter]
    permission_classes = [IsAuthenticated]
