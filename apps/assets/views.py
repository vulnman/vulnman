from django.urls import reverse_lazy
from vulnman.views import generic
from apps.assets import models
from apps.assets import forms


class WebApplicationList(generic.ProjectListView):
    template_name = "assets/webapp_list.html"
    context_object_name = "webapps"
    
    def get_queryset(self):
        return models.WebApplication.objects.filter(project=self.get_project())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["webapp_create_form"] = forms.WebApplicationForm()
        return context


class WebApplicationCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    form_class = forms.WebApplicationForm
    success_url = reverse_lazy("projects:assets:webapp-list")

    def get_queryset(self):
        return models.WebApplication.objects.filter(project=self.get_project())

    def form_valid(self, form):
        form.instance.project = self.get_project()
        return super().form_valid(form)


class WebApplicationUpdate(generic.ProjectUpdateView):
    form_class = forms.WebApplicationUpdateForm
    success_url = reverse_lazy("projects:assets:webapp-list")
    template_name = "assets/webapp_create.html"

    def get_queryset(self):
        return models.WebApplication.objects.filter(project=self.get_project())
        

class WebRequestList(generic.ProjectListView):
    template_name = "assets/webreqests_list.html"
    context_object_name = "webrequests"
    
    def get_queryset(self):
        return models.WebRequest.objects.filter(project=self.get_project())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["webrequest_create_form"] = forms.WebRequestCreateForm(self.get_project())
        return context


class WebRequestCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    form_class = forms.WebRequestCreateForm
    success_url = reverse_lazy("projects:assets:webrequest-list")

    def get_queryset(self):
        return models.WebRequest.objects.filter(project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class HostList(generic.ProjectListView):
    template_name = "assets/host_list.html"
    context_object_name = "hosts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host_create_form"] = forms.HostCreateForm(self.get_project()) 
        return context

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())


class HostCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    form_class = forms.HostCreateForm
    success_url = reverse_lazy("projects:assets:host-list")

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class ServiceList(generic.ProjectListView):
    template_name = "assets/service_list.html"
    context_object_name = "services"
    
    def get_queryset(self):
        return models.Service.objects.filter(project=self.get_project())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service_create_form"] = forms.ServiceCreateForm(self.get_project())
        return context


class ServiceCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    form_class = forms.ServiceCreateForm
    success_url = reverse_lazy("projects:assets:service-list")

    def get_queryset(self):
        return models.Service.objects.filter(project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs