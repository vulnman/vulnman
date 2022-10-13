import django_filters.views
from django.urls import reverse_lazy
from vulnman.core.views import generics
from vulnman.core.breadcrumbs import Breadcrumb
from apps.assets import models
from apps.assets import forms
from apps.assets import filters


class WebApplicationList(generics.ProjectListView):
    template_name = "assets/web_application/list.html"
    context_object_name = "webapps"

    def get_queryset(self):
        return models.WebApplication.objects.filter(project=self.get_project())


class WebApplicationCreate(generics.ProjectCreateView):
    form_class = forms.WebApplicationForm
    template_name = "core/pages/create.html"
    page_title = "Create Web Application"
    breadcrumbs = [
        Breadcrumb(reverse_lazy("projects:assets:webapp-list"), "Web Applications")
    ]


class WebApplicationUpdate(generics.ProjectUpdateView):
    form_class = forms.WebApplicationForm
    template_name = "core/pages/update.html"
    page_title = "Update Web Application"

    def get_breadcrumbs(self):
        return [
            Breadcrumb(reverse_lazy("projects:assets:webapp-list"), "Web Applications"),
            Breadcrumb(reverse_lazy("projects:assets:webapp-detail", kwargs={"pk": self.kwargs.get("pk")}),
                       self.get_object())
        ]

    def get_queryset(self):
        return models.WebApplication.objects.filter(project=self.get_project())


class HostList(generics.ProjectListView):
    # TODO: write tests
    template_name = "assets/host/list.html"
    context_object_name = "hosts"

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())


class HostCreate(generics.ProjectCreateView):
    # TODO: write tests
    form_class = forms.HostForm
    template_name = "core/pages/create.html"
    page_title = "Create Host"
    breadcrumbs = [
        Breadcrumb(reverse_lazy("projects:assets:host-list"), "Hosts")
    ]

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())


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
    template_name = "core/pages/create.html"
    page_title = "Create Service"
    breadcrumbs = [
        Breadcrumb(reverse_lazy("projects:assets:service-list"), "Services")
    ]

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
    template_name = "assets/host/detail.html"
    context_object_name = "host"

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
    form_class = forms.HostForm
    template_name = "core/pages/update.html"
    page_title = "Update Host"

    def get_breadcrumbs(self):
        return [
            Breadcrumb(reverse_lazy("projects:assets:host-list"), "Hosts"),
            Breadcrumb(reverse_lazy("projects:assets:host-detail", kwargs={"pk": self.kwargs.get("pk")}),
                       self.get_object())
        ]

    def get_queryset(self):
        return models.Host.objects.filter(project=self.get_project())


class ServiceUpdate(generics.ProjectUpdateView):
    form_class = forms.ServiceForm
    template_name = "core/pages/update.html"

    def get_breadcrumbs(self):
        return [
            Breadcrumb(reverse_lazy("projects:assets:service-list"), "Services"),
            Breadcrumb(reverse_lazy("projects:assets:service-detail", kwargs={"pk": self.kwargs.get("pk")}),
                       self.get_object())
        ]

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
