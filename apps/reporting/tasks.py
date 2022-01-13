from celery import shared_task
from django.conf import settings
from django.utils.module_loading import import_string
from apps.projects.models import Project
from django.contrib.auth.models import User
from apps.reporting.models import Report
from apps.reporting.utils.converter import HTMLConverter


@shared_task
def do_create_report(report_pk):
    report = Report.objects.get(pk=report_pk)
    context = {
        "REPORT_COMPANY_INFORMATION": settings.REPORT_COMPANY_INFORMATION,
        "SEVERITY_COLORS": settings.SEVERITY_COLORS,
        "report": report, "project": report.project
    }
    report_template = import_string(settings.REPORTING_TEMPLATE)()
    converter = HTMLConverter(report_template, context)
    raw_source, pdf_source = converter.convert()
    report.raw_source = raw_source
    report.pdf_source = pdf_source
    report.save()
