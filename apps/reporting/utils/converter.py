from weasyprint import HTML
from django.conf import settings
from django.template.loader import render_to_string


class HTMLConverter(object):
    def __init__(self, template_name, context):
        self.template_name = template_name
        self.context = context

    def convert(self):
        raw_source = render_to_string(self.template_name, self.context)
        pdf_source = HTML(string=raw_source).write_pdf(stylesheets=settings.REPORT_TEMPLATE_STYLESHEETS)
        return raw_source, pdf_source
