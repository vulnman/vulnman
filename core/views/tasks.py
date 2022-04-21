import django_filters.views
from vulnman.views import generic
from core import models
from core.forms import tasks as forms
from apps.methodologies import filters


class ProjectTaskList(django_filters.views.FilterMixin, generic.ProjectListView):
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


class ProjectTaskDetail(generic.ProjectDetailView):
    context_object_name = "task"
    model = models.AssetTask
    template_name = "tasks/project_task_detail.html"


class ProjectTaskStatusUpdate(generic.ProjectUpdateView):
    http_method_names = ["post"]
    form_class = forms.ProjectTaskStatusUpdateForm
    model = models.AssetTask

    def get_success_url(self):
        obj = self.get_object()
        return obj.get_absolute_url()
