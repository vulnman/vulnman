import os
from django.conf import settings
from apps.reporting.utils.report_template import ReportSection, ReportTemplate


class DefaultReportTemplate(ReportTemplate):
    name = "default-html-template"
    template_directory = os.path.join(settings.BASE_DIR, "vulnman/report_templates/default")
    sections = [
        ReportSection("Cover", "cover.html", None),
        ReportSection("Assessment Information", "assessment_information.html", None),
        ReportSection("Assessment Overview", "generic_md_section.html", "default.md"),
        ReportSection("Methodology", "generic_md_section.html", "default.md"),
        ReportSection("Vulnerability Overview", "vulnerability_overview.html", None),
        ReportSection("Vulnerability Listing", "vulnerability_listing.html", None)
    ]
    stylesheets = [
        "report.css"
    ]
