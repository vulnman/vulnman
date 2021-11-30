from vulnman.views import generic
from django.conf import settings
from django.urls import reverse_lazy
from django_tex.response import PDFResponse
from django_tex.shortcuts import compile_template_to_pdf
from django_tex.core import render_template_with_context, run_tex
from apps.reporting import models, forms


class ReportList(generic.ProjectListView):
    template_name = "reporting/report_list.html"
    paginate_by = 20
    context_object_name = "reports"

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project()).order_by('-revision')


class ReportDetail(generic.ProjectDetailView):
    template_name = "report/document.tex"
    context_object_name = "report"

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project())

    def render_to_response(self, context, **response_kwargs):
        return PDFResponse(context['report'].pdf_source, filename="report.pdf")


class ReportCreate(generic.ProjectCreateView):
    report_template_name = "report/document.tex"
    template_name = "reporting/report_create.html"
    form_class = forms.ReportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SEVERITY_COLORS'] = settings.SEVERITY_COLORS
        return context

    def get_success_url(self):
        return reverse_lazy('projects:reporting:report-list')

    def form_valid(self, form):
        form.instance.project = self.get_project()
        form.instance.creator = self.request.user
        form.save()
        context = self.get_context_data()
        context['report'] = form.instance
        pdf_source = compile_template_to_pdf(self.report_template_name, context)
        latex_source = render_template_with_context(self.report_template_name, context)
        form.instance.latex_source = latex_source
        form.instance.pdf_source = pdf_source
        return super().form_valid(form)


class ReportUpdate(generic.ProjectUpdateView):
    template_name = "reporting/report_update.html"
    report_template_name = "report/document.tex"
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
