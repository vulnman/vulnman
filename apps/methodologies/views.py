from django.urls import reverse_lazy
from vulnman.views import generic
from apps.methodologies import forms
from apps.methodologies import models


class MethodologyList(generic.VulnmanAuthListView):
    template_name = "methodologies/methodology_list.html"
    context_object_name = "methodologies"
    model = models.Task
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}


class MethodologyDetail(generic.VulnmanAuthDetailView):
    template_name = "methodologies/methodology_detail.html"
    context_object_name = "methodology"
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}


class MethodologyUpdate(generic.VulnmanAuthUpdateWithInlinesView):
    template_name = "methodologies/methodology_create.html"
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}


class MethodologyDelete(generic.VulnmanAuthDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy('methodology:methodology-list')


class MethodologyCreate(generic.VulnmanAuthCreateWithInlinesView):
    template_name = "methodologies/methodology_create.html"
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ProjectMethodologyList(generic.ProjectListView):
    template_name = "methodologies/project_methodology_list.html"
    context_object_name = "methodologies"
    allowed_project_roles = ["pentester"]


class ProjectMethodologyDetail(generic.ProjectDetailView):
    template_name = "methodologies/project_methodology_detail.html"
    context_object_name = "methodology"
    allowed_project_roles = ["pentester"]


class ProjectMethodologyCreate(generic.ProjectCreateWithInlinesView):
    template_name = "methodologies/project_methodology_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def forms_valid(self, form, inlines):
        response = self.form_valid(form)
        for formset in inlines:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.project = self.get_project()
                instance.creator = self.request.user
                instance.save()
        return response


class ProjectMethodologyDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy('projects:methodology:project-methodology-list')
    allowed_project_roles = ["pentester"]


class ProjectMethodologyUpdate(generic.ProjectUpdateWithInlinesView):
    template_name = "methodologies/project_methodology_create.html"


class ProjectMethodologyFromTemplateCreate(generic.ProjectFormView):
    http_method_names = ["post"]
    allowed_project_roles = ["pentester"]
    success_url = reverse_lazy("projects:methodology:project-methodology-list")

    def form_valid(self, form):
        methodology = form.cleaned_data["template"]
        return super().form_valid(form)
