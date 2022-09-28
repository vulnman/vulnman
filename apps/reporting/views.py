from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django_q.tasks import async_task
from vulnman.core.views import generics
from vulnman.core.breadcrumbs import Breadcrumb
from apps.reporting import models, forms
from apps.reporting import tasks


class ReportList(generics.ProjectListView):
    template_name = "reporting/report_list.html"
    context_object_name = "reports"

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project())


class ReportCreate(generics.ProjectCreateView):
    template_name = "reporting/report_create.html"
    form_class = forms.ReportCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.get_project()
        return kwargs


class ReportManagementSummary(generics.ProjectUpdateView):
    template_name = "reporting/report_management_summary.html"
    form_class = forms.ReportManagementSummaryForm

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project())


class ReportReleaseList(generics.ProjectListView):
    # TODO: write tests
    template_name = "reporting/report_releases.html"
    context_object_name = "releases"

    def get_context_data(self, **kwargs):
        kwargs["report"] = models.Report.objects.get(pk=self.kwargs.get("pk"), project=self.get_project())
        kwargs["wip_form"] = forms.ReportReleaseWIPForm()
        qs = models.ReportRelease.objects.filter(
            report__pk=self.kwargs.get("pk"), work_in_progress=True, report__project=self.get_project())
        if qs.exists():
            kwargs["wip_report"] = qs.get()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return models.ReportRelease.objects.filter(report__pk=self.kwargs.get("pk"),
                                                   work_in_progress=False,
                                                   report__project=self.get_project())


class ReportReleaseDelete(generics.ProjectDeleteView):
    # TODO: write tests
    http_method_names = ["post"]

    def get_queryset(self):
        return models.ReportRelease.objects.filter(report__project=self.get_project())

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-release-list", kwargs={"pk": self.get_object().report.pk})


class ReportReleaseCreate(generics.ProjectCreateView):
    # TODO: write tests
    template_name = "reporting/report_create.html"
    form_class = forms.ReportReleaseForm

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-release-list", kwargs={"pk": self.kwargs.get("pk")})

    def get_report(self):
        try:
            obj = models.Report.objects.get(pk=self.kwargs.get("pk"), project=self.get_project())
        except models.Report.DoesNotExist:
            return Http404()
        return obj

    def get_queryset(self):
        return models.ReportRelease.objects.filter(report__pk=self.kwargs.get("pk"))

    def form_valid(self, form):
        form.instance.project = self.get_project()
        form.instance.report = self.get_report()
        form.instance.creator = self.request.user
        instance = form.save()
        task_id = async_task(tasks.do_create_report, instance.pk)
        instance.task_id = task_id
        instance.save()
        return HttpResponseRedirect(self.get_success_url())


class ReportReleaseWIPCreate(generics.ProjectCreateView):
    # TODO: write tests
    template_name = "reporting/report_release_create.html"
    http_method_names = ["post"]
    form_class = forms.ReportReleaseWIPForm

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-release-list", kwargs={"pk": self.kwargs.get("pk")})

    def get_report(self):
        try:
            obj = models.Report.objects.get(pk=self.kwargs.get("pk"), project=self.get_project())
        except models.Report.DoesNotExist:
            return Http404()
        return obj

    def form_valid(self, form):
        qs = models.ReportRelease.objects.filter(report__pk=self.kwargs.get("pk"), project=self.get_project(),
                                                 work_in_progress=True)
        if qs.exists():
            qs.delete()
        form.instance.project = self.get_project()
        form.instance.report = self.get_report()
        form.instance.creator = self.request.user
        form.instance.name = "WIP"
        form.instance.release_type = models.ReportRelease.RELEASE_TYPE_DRAFT
        form.instance.work_in_progress = True
        instance = form.save()
        task_id = async_task(tasks.do_create_report, instance.pk)
        instance.task_id = task_id
        instance.save()
        return super().form_valid(form)


class ReportReleaseUpdate(generics.ProjectUpdateView):
    # TODO: write tests
    template_name = "reporting/report_release_update.html"
    form_class = forms.ReportReleaseUpdateForm

    def get_queryset(self):
        return models.ReportRelease.objects.filter(pk=self.kwargs.get("pk"), project=self.get_project())

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-release-list")


class ReportReleaseDetail(generics.ProjectDetailView):
    # TODO: write tests
    context_object_name = "report"

    def get_queryset(self):
        return models.ReportRelease.objects.filter(project=self.get_project())

    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        response = HttpResponse(obj.compiled_source, content_type=obj.report.get_report_content_type())
        response['Content-Disposition'] = 'attachment; filename="report.%s"' % obj.report.get_report_file_extension()
        return response

    def get_context_data(self, **kwargs):
        if self.request.session.get("active_report_task"):
            pass
        return super().get_context_data(**kwargs)


class ReportDelete(generics.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:reporting:report-list")

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project())


class VersionList(generics.ProjectListView):
    # TODO: write tests
    template_name = "reporting/version_list.html"
    context_object_name = "versions"

    def get_queryset(self):
        return models.ReportVersion.objects.filter(project=self.get_project(), report__pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        kwargs["report"] = models.Report.objects.get(pk=self.kwargs.get("pk"), project=self.get_project())
        return super().get_context_data(**kwargs)


class VersionCreate(generics.ProjectCreateView):
    # TODO: write tests
    template_name = "reporting/version_create.html"
    form_class = forms.VersionForm

    def get_queryset(self):
        return models.ReportVersion.objects.filter(project=self.get_project(), report__pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        kwargs["report"] = models.Report.objects.get(pk=self.kwargs.get("pk"), project=self.get_project())
        return super().get_context_data(**kwargs)

    def get_initial(self):
        initial = super().get_initial()
        report = models.Report.objects.get(pk=self.kwargs.get("pk"), project=self.get_project())
        initial["version"] = report.get_next_minor_version()
        return initial

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.report = context.get("report")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("projects:reporting:version-list", kwargs={"pk": self.kwargs.get("pk")})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.get_project()
        return kwargs


class VersionUpdate(generics.ProjectUpdateView):
    template_name = "core/pages/update.html"
    form_class = forms.VersionForm
    page_title = "Update Version"

    def get_breadcrumbs(self):
        report_pk = self.get_object().report.pk
        reports = Breadcrumb(reverse("projects:reporting:report-list"), "Reports")
        report = Breadcrumb(reverse("projects:reporting:report-detail", kwargs={"pk": report_pk}),
                            self.get_object().report.name)
        version_list = Breadcrumb(reverse("projects:reporting:version-list", kwargs={"pk": report_pk}), "Versions")
        return [reports, report, version_list]

    def get_success_url(self):
        return reverse_lazy("projects:reporting:version-list", kwargs={"pk": self.get_object().report.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.get_project()
        return kwargs

    def get_queryset(self):
        return models.ReportVersion.objects.filter(project=self.get_project(), pk=self.kwargs.get("pk"))


class VersionDelete(generics.ProjectDeleteView):
    # TODO: write tests
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("projects:reporting:version-list", kwargs={"pk": self.get_object().report.pk})

    def get_queryset(self):
        return models.ReportVersion.objects.filter(project=self.get_project(), pk=self.kwargs.get("pk"))
