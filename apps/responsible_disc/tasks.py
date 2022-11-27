from django.utils.module_loading import import_string
from django.conf import settings


def export_advisory(vulnerability):
    # returns a text or zip file
    # and a boolean that is set to true if it is a zip file
    template_name = vulnerability.advisory_template
    Report = import_string(settings.RESPONSIBLE_DISCLOSURE_ADVISORY_TEMPLATES.get(
        template_name, "default") + ".advisory.Report")
    obj = Report(None, template_name=template_name, vulnerability=vulnerability)
    raw_source, is_zip = obj.generate_report()
    return raw_source, is_zip
