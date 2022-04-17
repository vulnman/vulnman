from django.urls import reverse_lazy
from vulnman.views import generic
from apps.methodologies import forms
from apps.methodologies import models

class TaskList(generic.VulnmanAuthListView):
    template_name = "methodologies/methodology_list.html"
    context_object_name = "methodologies"
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}
    model = models.Task2


class ProjectToDos(generic.ProjectListView):
    template_name = "methodologies/project_tasks.html"
    context_object_name = "todos"
    model = models.AssetTask2
