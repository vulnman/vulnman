import django_filters.views
from vulnman.views import generic
from apps.methodologies import filters
from core import models


class TaskList(generic.VulnmanAuthListView):
    template_name = "methodologies/methodology_list.html"
    context_object_name = "methodologies"
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}
    model = models.Task


class ProjectToDos(django_filters.views.FilterMixin, generic.ProjectListView):
    template_name = "methodologies/project_tasks.html"
    context_object_name = "todos"
    model = models.AssetTask
    filterset_class = filters.ProjectTaskFilter

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).filter(
            project=self.get_project())
        filterset = self.filterset_class(
            self.request.GET, queryset=qs)
        return filterset.qs
