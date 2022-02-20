# TODO: legacy
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from dry_rest_permissions.generics import DRYPermissions
from vulnman.api.mixins import IgnoreFieldsAfterCreationMixin


class CreateListRetrieveViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]


class VulnmanModelViewSet(IgnoreFieldsAfterCreationMixin, ModelViewSet):
    permission_classes = [IsAuthenticated, DRYPermissions]
    filter_backends = [SearchFilter]
