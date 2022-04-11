from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter


class SearchModelViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    permission_classes = [IsAuthenticated]
