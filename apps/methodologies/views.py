from django.urls import reverse_lazy
from vulnman.views import generic
from apps.methodologies import forms
from apps.methodologies import models


class MethodologyList(generic.VulnmanAuthListView):
    template_name = "methodologies/methodology_list.html"
    model = models.Methodology
    context_object_name = "methodologies"
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}


class MethodologyDetail(generic.VulnmanAuthDetailView):
    template_name = "methodologies/methodology_detail.html"
    model = models.Methodology
    context_object_name = "methodology"
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}


class MethodologyUpdate(generic.VulnmanAuthUpdateWithInlinesView):
    template_name = "methodologies/methodology_create.html"
    model = models.Methodology
    inlines = [forms.TaskInline]
    form_class = forms.MethodologyForm
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}


class MethodologyDelete(generic.VulnmanAuthDeleteView):
    http_method_names = ["post"]
    model = models.Methodology
    success_url = reverse_lazy('methodology:methodology-list')


class MethodologyCreate(generic.VulnmanAuthCreateWithInlinesView):
    template_name = "methodologies/methodology_create.html"
    form_class = forms.MethodologyForm
    inlines = [forms.TaskInline]
    model = models.Methodology
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ProjectMethodologyList(generic.ProjectListView):
    template_name = "methodologies/project_methodology_list.html"
    context_object_name = "methodologies"
    allowed_project_roles = ["pentester"]

    def get_queryset(self):
        return models.ProjectMethodology.objects.filter(project=self.get_project())


class ProjectMethodologyDetail(generic.ProjectDetailView):
    template_name = "methodologies/project_methodology_detail.html"
    context_object_name = "methodology"
    allowed_project_roles = ["pentester"]

    def get_queryset(self):
        return models.ProjectMethodology.objects.filter(project=self.get_project(), pk=self.kwargs.get('pk'))


class ProjectMethodologyCreate(generic.ProjectCreateWithInlinesView):
    template_name = "methodologies/project_methodology_create.html"
    form_class = forms.ProjectMethodologyForm
    inlines = [forms.ProjectTaskInline]
    model = models.ProjectMethodology

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
    model = models.ProjectMethodology
    success_url = reverse_lazy('projects:methodology:project-methodology-list')
    allowed_project_roles = ["pentester"]

    def get_queryset(self):
        return models.ProjectMethodology.objects.filter(project=self.get_project(), pk=self.kwargs.get('pk'))


class ProjectMethodologyUpdate(generic.ProjectUpdateWithInlinesView):
    template_name = "methodologies/project_methodology_create.html"
    form_class = forms.ProjectMethodologyForm
    inlines = [forms.ProjectTaskInline]
    model = models.ProjectMethodology
