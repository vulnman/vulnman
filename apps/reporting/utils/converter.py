import os
from weasyprint import HTML
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template import engines
from vulnman.utils.markdown import bleach_md
from apps.reporting import models


class HTMLConverter(object):
    def __init__(self, template, context):
        self.template = template
        self.context = context
        self.report = context["report"]

    def convert(self):
        raw_source = render_to_string(self.template.get_template_path(), self.context)
        pdf_source = HTML(string=raw_source).write_pdf(stylesheets=self.template.get_stylesheet_paths())
        return raw_source, pdf_source
