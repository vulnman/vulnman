from rest_framework.filters import BaseFilterBackend


class ProjectRelatedFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        project = view.get_project()
        return queryset.filter(project=project)
