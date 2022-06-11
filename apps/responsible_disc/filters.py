import django_filters
from apps.responsible_disc import models


class VulnerabilityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.Vulnerability
        fields = ['name', "template__name", "template__vulnerability_id"]
