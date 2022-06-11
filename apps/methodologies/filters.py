import django_filters
from apps.methodologies import models


class ProjectTaskFilter(django_filters.FilterSet):
    name = django_filters.CharFilter("task__name", lookup_expr="icontains")

    class Meta:
        model = models.AssetTask
        fields = ["status", "name"]
