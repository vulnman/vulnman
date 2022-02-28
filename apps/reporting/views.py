from vulnman.views import generic
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.module_loading import import_string
from apps.reporting import models, forms
from apps.reporting.utils.converter import HTMLConverter
from apps.reporting import tasks


class ReportList(generic.ProjectListView):
    template_name = "reporting/report_list.html"
    paginate_by = 20
    context_object_name = "reports"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report_share_form"] = forms.ReportShareTokenForm()
        if len(self.get_queryset()):
            context["report_mgmt_summary_form"] = forms.ReportManagementSummaryForm(
                initial={"recommendation": self.get_project().reportinformation.recommendation,
                    "evaluation": self.get_project().reportinformation.evaluation
                })
        return context

    def get_queryset(self):
        return models.PentestReport.objects.filter(project=self.get_project())#.order_by('-revision')
<<<<<<< HEAD


class PentestReportDraftCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    form_class = forms.PentestReportDraftForm

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-list")

    def form_valid(self, form):
        if models.PentestReport.objects.filter(project=self.get_project()).exists():
            report = models.PentestReport.objects.get(project=self.get_project())
        else:
            form.instance.project = self.get_project()
            form.instance.creator = self.request.user
            form.instance.report_type = "draft"
            report = form.save()
        tasks.do_create_report.delay(report.pk)
        return HttpResponseRedirect(self.get_success_url())


class PentestReportDownload(generic.ProjectDetailView):
    context_object_name = "report"

    def get_queryset(self):
        return models.PentestReport.objects.filter(project=self.get_project())
    
    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        response = HttpResponse(obj.pdf_source, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response
=======
>>>>>>> origin/dev


class PentestReportDraftCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    form_class = forms.PentestReportDraftForm

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-list")

    def form_valid(self, form):
        tasks.do_create_report.delay(self.get_project().reportinformation.pk, "draft")
        return HttpResponseRedirect(self.get_success_url())


class PentestReportDownload(generic.ProjectDetailView):
    context_object_name = "report"

    def get_queryset(self):
        return models.PentestReport.objects.filter(project=self.get_project())
<<<<<<< HEAD

=======
    
>>>>>>> origin/dev
    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        response = HttpResponse(obj.pdf_source, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response


class ReportSharedDetail(generic.VulnmanDetailView):
    model = models.Report
    context_object_name = "report"

    def get_queryset(self):
        report = models.Report.objects.filter(pk=self.kwargs.get('pk'))
        try:
            obj = report.get()
            if obj.reportsharetoken.is_expired(self.kwargs.get('token')):
                return models.Report.objects.none()
        except models.Report.DoesNotExist:
            return models.Report.objects.none()
        return report

    def render_to_response(self, context, **response_kwargs):
        return PDFResponse(context['report'].pdf_source, filename="report.pdf")


class ReportSharedTokenCreate(generic.ProjectCreateView):
    model = models.ReportShareToken
    form_class = forms.ReportShareTokenForm
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:reporting:report-list")

    def form_valid(self, form):
        report = models.Report.objects.filter(pk=self.kwargs.get('pk'), project=self.get_project())
        if not report.exists():
            return super().form_invalid(form)
        form.instance.report = report.get()
        response = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Share Link: %s" % self.request.build_absolute_uri(
            reverse_lazy(
                "projects:reporting:report-shared-report-detail",
                kwargs={"pk": self.kwargs.get('pk'), "token": report.get().reportsharetoken.share_token})))
        return response
