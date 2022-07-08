import django_filters.views
from django.urls import reverse_lazy
from vulnman.core.views import generics
from apps.assets import models
from apps.assets import forms
from apps.assets import filters


class WebApplicationList(generics.ProjectListView):
    template_name = "assets/web_application/list.html"
    context_object_name = "webapps"

    def get_queryset(self):
        return models.WebApplication.objects.filter(project=self.get_project())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["webapp_create_form"] = forms.WebApplicationForm()
        return context


class WebApplicationCreate(generics.ProjectCreateView):
    form_class = forms.WebApplicationForm
    template_name = "assets/web_application/update.html"


class WebApplicationUpdate(generics.ProjectUpdateView):
    form_class = forms.WebApplicationForm
    template_name = "assets/web_application/update.html"

    def get_queryset(self):
        return models.WebApplication.objects.filter(project=self.get_project())


class WebRequestList(generics.ProjectListView):
    # TODO: write tests
    template_name = "assets/webrequest_list.html"
    context_object_name = "webrequests"

    def get_queryset(self):
        return models.WebRequest.objects.filter(project=self.get_project())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["webrequest_create_form"] = forms.WebRequestCreateForm(
            self.get_project())
        return context


class WebRequestCreate(generics.ProjectCreateView):
    # TODO: write tests
    http_method_names = ["post"]
    form_class = forms.WebRequestCreateForm
    success_url = reverse_lazy("projects:assets:webrequest-list")

    def get_queryset(self):
        return models.WebRequest.objects.filter(project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class HostList(generics.ProjectListView):
    # TODO: write tests
    template_name = "assets/host_list.html"
    context_object_name = "hosts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host_create_form"] = forms.HostCreateForm(self.get_project())
        return context

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())


class HostCreate(generics.ProjectCreateView):
    # TODO: write tests
    http_method_names = ["post"]
    form_class = forms.HostCreateForm
    success_url = reverse_lazy("projects:assets:host-list")

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class ServiceList(django_filters.views.FilterMixin, generics.ProjectListView):
    # TODO: write tests
    template_name = "assets/service/list.html"
    context_object_name = "services"
    filterset_class = filters.ServiceFilter
    model = models.Service

    def get_queryset(self):
        qs = super().get_queryset().filter(
            project=self.get_project())
        filterset = self.filterset_class(self.request.GET, queryset=qs)
        return filterset.qs


class ServiceCreate(generics.ProjectCreateView):
    form_class = forms.ServiceForm
    template_name = "assets/service/create_or_update.html"

    def get_queryset(self):
        return models.Service.objects.filter(project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class ServiceDetail(generics.ProjectDetailView):
    template_name = "assets/service/detail.html"
    context_object_name = "service"
    model = models.Service


class ServiceDelete(generics.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:assets:service-list")

    def get_queryset(self):
        return models.Service.objects.filter(project=self.get_project())


class HostDetail(generics.ProjectDetailView):
    # TODO: write tests
    template_name = "assets/host_detail.html"
    context_object_name = "host"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host_update_form"] = forms.HostUpdateForm(
            project=self.get_project(), instance=context["host"])
        return context

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())


class HostDelete(generics.ProjectDeleteView):
    # TODO: write tests
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:assets:host-list")

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())


class HostUpdate(generics.ProjectUpdateView):
    # TODO: write tests
    http_method_names = ["post"]
    form_class = forms.HostUpdateForm

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class ServiceUpdate(generics.ProjectUpdateView):
    form_class = forms.ServiceForm
    template_name = "assets/service/create_or_update.html"

    def get_queryset(self):
        return models.Service.objects.filter(project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


class WebApplicationDetail(generics.ProjectDetailView):
    template_name = "assets/web_application/detail.html"
    context_object_name = "webapp"
    model = models.WebApplication


class WebApplicationDelete(generics.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:assets:webapp-list")

    def get_queryset(self):
        return models.WebApplication.objects.filter(
            project=self.get_project())


class WebRequestDelete(generics.ProjectDeleteView):
    # TODO: write tests
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:assets:webrequest-list")

    def get_queryset(self):
        return models.WebRequest.objects.filter(
            project=self.get_project())


class WebRequestDetail(generics.ProjectDetailView):
    # TODO: write tests
    template_name = "assets/webrequest_detail.html"
    context_object_name = "webrequest"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["webrequest_update_form"] = forms.WebRequestUpdateForm(
            project=self.get_project(), instance=context["webrequest"])
        return context

    def get_queryset(self):
        return models.WebRequest.objects.filter(project=self.get_project())


class WebRequestUpdate(generics.ProjectUpdateView):
    # TODO: write tests
    http_method_names = ["post"]
    form_class = forms.WebRequestUpdateForm

    def get_queryset(self):
        return models.WebRequest.objects.filter(
            project=self.get_project())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs
