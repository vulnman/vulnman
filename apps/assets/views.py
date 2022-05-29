from django.urls import reverse_lazy
import django_filters.views
from vulnman.views import generic
from apps.assets import models
from apps.assets import forms
from apps.assets import filters


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
    template_name = "assets/webrequest_list.html"
    context_object_name = "webrequests"

    def get_queryset(self):
        return models.WebRequest.objects.filter(project=self.get_project())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["webrequest_create_form"] = forms.WebRequestCreateForm(
            self.get_project())
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


class ServiceList(django_filters.views.FilterMixin, generic.ProjectListView):
    template_name = "assets/service_list.html"
    context_object_name = "services"
    filterset_class = filters.ServiceFilter
    model = models.Service

    def get_queryset(self):
        qs = super().get_queryset().filter(
            project=self.get_project())
        filterset = self.filterset_class(self.request.GET, queryset=qs)
        return filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service_create_form"] = forms.ServiceCreateForm(
            self.get_project())
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


class ServiceDetail(generic.ProjectDetailView):
    template_name = "assets/service_detail.html"
    context_object_name = "service"

    def get_queryset(self):
        return models.Service.objects.filter(project=self.get_project())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service_update_form"] = forms.ServiceUpdateForm(
            project=self.get_project(), instance=context["service"])
        return context


class ServiceDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:assets:service-list")

    def get_queryset(self):
        return models.Service.objects.filter(project=self.get_project())


class HostDetail(generic.ProjectDetailView):
    template_name = "assets/host_detail.html"
    context_object_name = "host"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host_update_form"] = forms.HostUpdateForm(
            project=self.get_project(), instance=context["host"])
        return context

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())


class HostDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:assets:host-list")

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())


class HostUpdate(generic.ProjectUpdateView):
    http_method_names = ["post"]
    form_class = forms.HostUpdateForm

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class ServiceUpdate(generic.ProjectUpdateView):
    http_method_names = ["post"]
    form_class = forms.ServiceUpdateForm

    def get_queryset(self):
        return models.Service.objects.filter(project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class WebApplicationDetail(generic.ProjectDetailView):
    template_name = "assets/webapp_detail.html"
    context_object_name = "webapp"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["webapp_update_form"] = forms.WebApplicationUpdateForm(
            instance=context["webapp"])
        return context

    def get_queryset(self):
        return models.WebApplication.objects.filter(
            project=self.get_project())


class WebApplicationDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:assets:webapp-list")

    def get_queryset(self):
        return models.WebApplication.objects.filter(
            project=self.get_project())


class WebRequestDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:assets:webrequest-list")

    def get_queryset(self):
        return models.WebRequest.objects.filter(
            project=self.get_project())


class WebRequestDetail(generic.ProjectDetailView):
    template_name = "assets/webrequest_detail.html"
    context_object_name = "webrequest"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["webrequest_update_form"] = forms.WebRequestUpdateForm(
            project=self.get_project(), instance=context["webrequest"])
        return context

    def get_queryset(self):
        return models.WebRequest.objects.filter(project=self.get_project())


class WebRequestUpdate(generic.ProjectUpdateView):
    http_method_names = ["post"]
    form_class = forms.WebRequestUpdateForm

    def get_queryset(self):
        return models.WebRequest.objects.filter(
            project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs
