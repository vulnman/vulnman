from vulnman.views import generic
from core import models


class ProjectTaskList(generic.ProjectListView):
    context_object_name = "tasks"
    model = models.AssetTask
    template_name = "tasks/project_task_list.html"


class ProjectTaskDetail(generic.ProjectDetailView):
    context_object_name = "task"
    model = models.AssetTask
    template_name = "tasks/project_task_detail.html"
