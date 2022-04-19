from django.urls import reverse_lazy
from vulnman.views import generic
from core import models
from core.forms import tasks as forms


class ProjectTaskList(generic.ProjectListView):
    context_object_name = "tasks"
    model = models.AssetTask
    template_name = "tasks/project_task_list.html"


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
