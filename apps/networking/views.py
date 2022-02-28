from django.urls import reverse_lazy
from vulnman.views import generic
from apps.networking import models
from apps.networking import forms


class HostList(generic.ProjectListView):
    template_name = "networking/host_list.html"
    context_object_name = "hosts"
    model = models.Host
    allowed_project_roles = ["pentester", "read-only"]


class HostCreate(generic.ProjectCreateWithInlinesView):
    template_name = "networking/host_create.html"
    form_class = forms.HostForm
    model = models.Host
    inlines = [forms.HostnameInline]
    allowed_project_roles = ["pentester"]

    def forms_valid(self, form, inlines):
        response = self.form_valid(form)
        for formset in inlines:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.project = self.get_project()
                instance.save()
        return response


class HostDetail(generic.ProjectDetailView):
    template_name = "networking/host_detail.html"
    context_object_name = "host"
    model = models.Host


class HostEdit(generic.ProjectUpdateWithInlinesView):
    template_name = "networking/host_create.html"
    form_class = forms.HostForm
    model = models.Host
    inlines = [forms.HostnameInline]
    allowed_project_roles = ["pentester"]


class HostDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    model = models.Host
    success_url = reverse_lazy('projects:networking:host-list')
    allowed_project_roles = ["pentester"]
