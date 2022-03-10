from celery import shared_task
from django.conf import settings
from django.db.models import Q
from django.utils.module_loading import import_string
from apps.projects.models import Project
from django.contrib.auth.models import User
from apps.reporting.models import PentestReport, ReportInformation
from apps.findings.models import Template, Vulnerability
from apps.reporting.utils.converter import HTMLConverter
from apps.reporting.utils import charts


@shared_task
def do_create_report(report_pk, report_type, creator=None):
    reportinformation = ReportInformation.objects.get(pk=report_pk)
    project = reportinformation.get_project()
    template_pks = Template.objects.filter(vulnerability__project=project).order_by('-severity').values_list("pk", flat=True)
    unique_pks = []
    for template_pk in template_pks:
        if not template_pk in unique_pks:
            unique_pks.append(template_pk)
    templates = []
    for pk in unique_pks:
        templates.append(Template.objects.get(pk=pk))
    context = {
        "REPORT_COMPANY_INFORMATION": settings.REPORT_COMPANY_INFORMATION,
        "creator": creator,
        "SEVERITY_COLORS": settings.SEVERITY_COLORS, 'templates': templates,
        "report": reportinformation, "project": project, 'report_type': report_type,
        'SEVERITY_CHART_SRC': charts.SeverityDonutChart().create_image(project),
        'CATEGORY_POLAR_CHART': charts.VulnCategoryPolarChart().create_image(project)
    }
    report_template = import_string(settings.REPORTING_TEMPLATE)()
    converter = HTMLConverter(report_template, context)
    raw_source, pdf_source = converter.convert()
    if report_type == "draft":
        if PentestReport.objects.filter(project=project).exists():
            report = PentestReport.objects.get(project=project, report_type="draft")
            report.raw_source = raw_source
            report.pdf_source = pdf_source
            report.save()
        else:
            report = PentestReport.objects.create(project=project, report_type="draft", raw_source=raw_source, pdf_source=pdf_source)
    else:
        print("Not yet implemented")
