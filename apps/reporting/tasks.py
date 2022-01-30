from celery import shared_task
from django.conf import settings
from django.utils.module_loading import import_string
from apps.projects.models import Project
from django.contrib.auth.models import User
from apps.reporting.models import Report
from apps.findings.models import Template
from apps.reporting.utils.converter import HTMLConverter
from apps.reporting.utils.charts import SeverityDonutChart


@shared_task
def do_create_report(report_pk):
    report = Report.objects.get(pk=report_pk)
    template_pks = Template.objects.filter(vulnerability__project=report.project, vulnerability__verified=True).order_by('-vulnerability__cvss_score').values_list("pk", flat=True)
    unique_pks = []
    for template_pk in template_pks:
        if not template_pk in unique_pks:
            unique_pks.append(template_pk)
    templates = []
    for pk in unique_pks:
        templates.append(Template.objects.get(pk=pk))

    context = {
        "REPORT_COMPANY_INFORMATION": settings.REPORT_COMPANY_INFORMATION,
        "SEVERITY_COLORS": settings.SEVERITY_COLORS, 'templates': templates,
        "report": report, "project": report.project,
        'SEVERITY_CHART_SRC': SeverityDonutChart().create_image(report.project)
    }
    report_template = import_string(settings.REPORTING_TEMPLATE)()
    converter = HTMLConverter(report_template, context)
    raw_source, pdf_source = converter.convert()
    report.raw_source = raw_source
    report.pdf_source = pdf_source
    report.save()
