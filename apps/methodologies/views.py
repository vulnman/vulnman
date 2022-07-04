import django_filters.views
from vulnman.core.views import generics
from apps.methodologies import filters
from apps.methodologies import forms
from apps.methodologies import models


class TaskList(generics.VulnmanAuthListView):
    # TODO: write tests
    template_name = "methodologies/methodology_list.html"
    context_object_name = "methodologies"
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}
    model = models.Task


class ProjectToDos(django_filters.views.FilterMixin, generics.ProjectListView):
    # TODO: write tests
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


class ProjectTaskList(django_filters.views.FilterMixin, generics.ProjectListView):
    # TODO: write tests
    context_object_name = "tasks"
    model = models.AssetTask
    template_name = "tasks/project_task_list.html"
    filterset_class = filters.ProjectTaskFilter

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).filter(
            project=self.get_project())
        filterset = self.filterset_class(
            self.request.GET, queryset=qs)
        return filterset.qs


class ProjectTaskDetail(generics.ProjectDetailView):
    # TODO: write tests
    context_object_name = "task"
    model = models.AssetTask
    template_name = "tasks/project_task_detail.html"


class ProjectTaskStatusUpdate(generics.ProjectUpdateView):
    # TODO: write tests
    http_method_names = ["post"]
    form_class = forms.ProjectTaskStatusUpdateForm
    model = models.AssetTask

    def get_success_url(self):
        obj = self.get_object()
        return obj.get_absolute_url()
