from django.conf import settings
from django.utils import translation
from django.utils.module_loading import import_string
from apps.reporting import models


def export_single_vulnerability(vulnerability, template_name):
    Report = import_string(settings.REPORT_TEMPLATES.get(template_name, "default") + ".vulnerability_report.Report")
    obj = Report(None, template_name=template_name, vulnerability=vulnerability)
    _raw_source, compiled_source = obj.generate_report()
    return compiled_source


def do_create_report(report_release_pk):
    """Task for creating PDF pentest reports
    """
    try:
        report_release = models.ReportRelease.objects.get(pk=report_release_pk)
    except models.ReportRelease.DoesNotExist:
        return False, "No such report release found!"

    # activate django language support in celery task
    translation.activate(report_release.report.language)

    report_variant = report_release.get_report_variant()
    result = report_variant.generate()
    return result
