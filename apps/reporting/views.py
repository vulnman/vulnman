from vulnman.views import generic
from django.conf import settings
from django.urls import reverse_lazy
from django_tex.response import PDFResponse
from django_tex.shortcuts import compile_template_to_pdf
from django_tex.core import render_template_with_context, run_tex
from apps.reporting import models, forms
from apps.reporting.utils.converter import HTMLConverter


class ReportList(generic.ProjectListView):
    template_name = "reporting/report_list.html"
    paginate_by = 20
    context_object_name = "reports"
    allowed_project_roles = ["read-only", "pentester"]

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project()).order_by('-revision')


class ReportDetail(generic.ProjectDetailView):
    context_object_name = "report"
    allowed_project_roles = ["pentester"]

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project())

    def render_to_response(self, context, **response_kwargs):
        return PDFResponse(context['report'].pdf_source, filename="report.pdf")


class ReportCreate(generic.ProjectCreateView):
    report_template_name = settings.REPORT_TEMPLATE
    template_name = "reporting/report_create.html"
    form_class = forms.ReportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SEVERITY_COLORS'] = settings.SEVERITY_COLORS
        context['REPORT_COMPANY_INFORMATION'] = settings.REPORT_COMPANY_INFORMATION
        context['REPORT_SECTIONS'] = {}
        for key, value in settings.REPORT_SECTIONS.items():
            with open(value, "r") as f:
                context['REPORT_SECTIONS'][key] = f.read()
        return context

    def get_success_url(self):
        return reverse_lazy('projects:reporting:report-list')

    def form_valid(self, form):
        form.instance.project = self.get_project()
        form.instance.creator = self.request.user
        form.save()
        context = self.get_context_data()
        context['report'] = form.instance
        if self.report_template_name.endswith(".html"):
            converter = HTMLConverter(self.report_template_name, context)
            raw_source, pdf_source = converter.convert()
        else:
            pdf_source = compile_template_to_pdf(self.report_template_name, context)
            raw_source = render_template_with_context(self.report_template_name, context)
        form.instance.raw_source = raw_source
        form.instance.pdf_source = pdf_source
        return super().form_valid(form)


class ReportUpdate(generic.ProjectUpdateView):
    template_name = "reporting/report_update.html"
    report_template_name = settings.REPORT_TEMPLATE
    form_class = forms.ReportUpdateForm

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project())

    def form_valid(self, form):
        try:
            pdf_source = run_tex(form.instance.latex_source)
            form.instance.pdf_source = pdf_source
            return super().form_valid(form)
        except Exception as e:
            form.instance.delete()
            form.delete()
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('projects:reporting:report-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SEVERITY_COLORS'] = settings.SEVERITY_COLORS
        return context


class ReportDraftDelete(generic.ProjectDeleteView):
    model = models.Report
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy('projects:reporting:report-list')

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project(), is_draft=True, pk=self.kwargs.get('pk'))
