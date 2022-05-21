import os
from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from apps.reporting.models import PentestReport, ReportInformation
from apps.findings.models import Template
from apps.reporting.utils import charts


def get_sorted_vuln_templates(project):
    """Get vulnerability templates sorted by severity

    Args:
        project (_type_): _description_
    """
    template_pks = Template.objects.filter(
        vulnerability__project=project).order_by(
            "-severity").values_list("pk", flat=True)
    unique_pks = []
    for template_pk in template_pks:
        if template_pk not in unique_pks:
            unique_pks.append(template_pk)
    templates = []
    for primary_key in unique_pks:
        templates.append(
            Template.objects.get(pk=primary_key))
    return templates


def get_stylesheets(report_template):
    """get full path of report stylesheets for weasyprint

    Args:
        report_template (_type_): _description_

    Returns:
        _type_: _description_
    """
    css_paths = []
    report_template_path = "resources/report_templates/" + report_template
    css_list = settings.REPORT_TEMPLATES.get(report_template).get("CSS", [])
    for css in css_list:
        css_paths.append(
            os.path.join(settings.BASE_DIR, report_template_path + "/" + css)
        )
    return css_paths


@shared_task
def export_single_vulnerability(vulnerability):
    context = {
        "vulnerability": vulnerability,
        "REPORT_COMPANY_INFORMATION": settings.REPORT_COMPANY_INFORMATION,
    }
    # TODO: do not hardcode this one
    report_template = "default"
    template = "default/exported_vulnerability.html"
    raw_source = render_to_string(template, context)
    font_config = FontConfiguration()
    pdf_source = HTML(string=raw_source).write_pdf(
        stylesheets=get_stylesheets(report_template),
        font_config=font_config)
    return pdf_source


@shared_task
def do_create_report(report_pk, report_type, report_template=None, creator=None, name=None):
    """Celery task for create PDF pentesting reports

    Args:
        report_pk (str): _description_
        report_type (str): _description_
        creator (User, optional): _description_. Defaults to None.
    """
    if not report_template:
        report_template = "default"
    reportinformation = ReportInformation.objects.get(pk=report_pk)
    project = reportinformation.get_project()
    templates = get_sorted_vuln_templates(project)
    context = {
        "REPORT_COMPANY_INFORMATION": settings.REPORT_COMPANY_INFORMATION,
        "creator": creator,
        'templates': templates,
        "report": reportinformation, "project": project,
        'report_type': report_type,
        'SEVERITY_CHART_SRC': charts.SeverityDonutChart().create_image(
            project),
        'CATEGORY_POLAR_CHART': charts.VulnCategoryPolarChart().create_image(
            project)
    }
    jinja_template = report_template +\
        "/report.html"
    raw_source = render_to_string(jinja_template, context)
    font_config = FontConfiguration()
    pdf_source = HTML(string=raw_source).write_pdf(
        stylesheets=get_stylesheets(report_template),
        font_config=font_config)
    if report_type == "draft":
        qs = PentestReport.objects.filter(project=project)
        if qs.exists() and not name:
            report = PentestReport.objects.get(
                project=project, report_type="draft", name="")
            report.raw_source = raw_source
            report.pdf_source = pdf_source
            report.save()
        else:
            if not name:
                # work in progress report
                PentestReport.objects.create(
                    project=project, report_type="draft",
                    raw_source=raw_source,
                    pdf_source=pdf_source)
            else:
                PentestReport.objects.create(
                    project=project, report_type="draft",
                    raw_source=raw_source, name=name,
                    pdf_source=pdf_source)
    else:
        PentestReport.objects.create(
            project=project, name=name, report_type=report_type,
            raw_source=raw_source, pdf_source=pdf_source)
