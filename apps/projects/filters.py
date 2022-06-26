import django_filters
from django.db.models import Q
from apps.projects import models


class ProjectFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search_filter')
    sort = django_filters.CharFilter(method='sort_filter')
    name = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.ChoiceFilter(choices=models.Project.PENTEST_STATUS_CHOICES)

    class Meta:
        model = models.Project
        fields = ['q', 'sort']

    def search_filter(self, queryset, _name, value):
        qs = queryset.filter(
            Q(client__name__icontains=value) |
            Q(name__icontains=value)
        )
        return qs

    def sort_filter(self, queryset, name, value):
        if value == "recently_updated":
            qs = queryset.order_by("-date_updated")
        elif value == "severity":
            qs = queryset.order_by("-severity")
        else:
            qs = queryset
        return qs
