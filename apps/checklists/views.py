from vulnman.core.views import generics
from vulnman.core.breadcrumbs import Breadcrumb
from django.urls import reverse_lazy
from . import models
from . import forms


class ProjectChecklistList(generics.ProjectListView):
    template_name = "checklists/list.html"

    def get_queryset(self):
        return models.ProjectTask.objects.filter(project=self.get_project())


class ProjectChecklistCreate(generics.ProjectCreateView):
    form_class = forms.ChecklistForm
    template_name = "core/pages/create.html"
    page_title = "Create Checklist"
    breadcrumbs = [
        Breadcrumb(reverse_lazy("projects:checklists:checklists-list"), "Checklists")
    ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.get_project()
        return kwargs
