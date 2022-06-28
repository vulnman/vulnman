from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.urls import reverse_lazy
from vulnman.views import generic
from apps.reporting import models, forms
from apps.reporting import tasks


class ReportList(generic.ProjectListView):
    template_name = "reporting/report_list.html"
    paginate_by = 20
    context_object_name = "reports"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if len(self.get_queryset()):
        context["report_mgmt_summary_form"] = forms.ReportManagementSummaryForm(
            initial={
                "recommendation": self.get_project().reportinformation.recommendation,
                "evaluation": self.get_project().reportinformation.evaluation
            })
        context["report_create_form"] = forms.PentestReportForm()
        return context

    def get_queryset(self):
        return models.PentestReport.objects.filter(~Q(name=""), project=self.get_project())


class PentestReportDraftCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    form_class = forms.PentestReportDraftForm

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-list")

    def form_valid(self, form):
        tasks.do_create_report.delay(
            self.get_project().reportinformation.pk, "draft",
            creator=self.request.user.username)
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


class PentestReportCreate(generic.ProjectCreateView):
    http_method_names = ["post"]
    form_class = forms.PentestReportForm

    def get_success_url(self):
        return reverse_lazy("projects:reporting:report-list")

    def form_valid(self, form):
        tasks.do_create_report.delay(
            self.get_project().reportinformation.pk,
            form.cleaned_data["report_type"],
            self.request.build_absolute_uri() + self.request.user.profile.get_absolute_url(),
            creator=self.request.user.username,
            name=form.cleaned_data["name"],
            language=form.cleaned_data["language"]
        )
        return HttpResponseRedirect(self.get_success_url())


class PentestReportDelete(generic.ProjectDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("projects:reporting:report-list")

    def get_queryset(self):
        return models.PentestReport.objects.filter(project=self.get_project())
