from django.conf import settings
from django.utils import translation
from django.template.loader import render_to_string
from apps.reporting import models
from apps.findings.models import Template
from apps.reporting.utils import charts, report_gen


def export_single_vulnerability(vulnerability):
    context = {
        "vulnerability": vulnerability,
        "REPORT_COMPANY_INFORMATION": settings.REPORT_COMPANY_INFORMATION,
    }
    # TODO: do not hardcode this one
    report_template = "default"
    template = "report_templates/default/exported_vulnerability.html"
    raw_source = render_to_string(template, context)
    report_generator = report_gen.ReportGenerator(report_template)
    compiled_source = report_generator.generate(raw_source)
    return compiled_source


def do_create_report(report_release_pk):
    """Celery task for create PDF pentest reports
    """
    try:
        report_release = models.ReportRelease.objects.get(pk=report_release_pk)
    except models.ReportRelease.DoesNotExist:
        return False, "No such report release found!"

    # activate django language support in celery task
    translation.activate(report_release.report.language)

    # load vulnerability templates
    project = report_release.project
    vulnerability_templates = Template.objects.unique_and_ordered_for_project(project)

    context = {
        "REPORT_COMPANY_INFORMATION": settings.REPORT_COMPANY_INFORMATION,
        "templates": vulnerability_templates, "release": report_release,
        "project": project, "SEVERITY_CHART_SRC": charts.SeverityDonutChart().create_image(project),
        "CATEGORY_POLAR_CHART": charts.VulnCategoryPolarChart().create_image(project)
    }

    jinja_template = "report_templates/" + report_release.report.template + "/report.html"
    raw_source = render_to_string(jinja_template, context)

    report_generator = report_gen.ReportGenerator(report_release.report.template)
    compiled_source = report_generator.generate(raw_source)

    report_release.raw_source = raw_source
    report_release.compiled_source = compiled_source
    report_release.task_id = None
    report_release.save()
    return True, "Report Release created!"
