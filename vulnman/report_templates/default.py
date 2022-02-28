import os
from django.conf import settings
from apps.reporting.utils.report_template import ReportTemplate


class DefaultReportTemplate(ReportTemplate):
    name = "default-html-template"
    template_directory = os.path.join(settings.BASE_DIR, "vulnman/report_templates/default")
    stylesheets = [
        "report.css"
    ]
