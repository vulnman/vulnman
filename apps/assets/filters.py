import django_filters
from apps.assets import models


class ServiceFilter(django_filters.FilterSet):
    ip = django_filters.CharFilter("host__ip", lookup_expr="icontains")
    class Meta:
        model = models.Service
        fields = ["ip", "port", "name"]
