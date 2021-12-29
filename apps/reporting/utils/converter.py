import os
from weasyprint import HTML
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template import engines
from vulnman.utils.markdown import bleach_md
from apps.reporting import models


class HTMLConverter(object):
    def __init__(self, template_name, context):
        self.template_name = template_name
        self.context = context
        self.report = context["report"]

    def convert(self):
        self.render_sections()
        raw_source = render_to_string(self.template_name, self.context)
        pdf_source = HTML(string=raw_source).write_pdf(stylesheets=settings.REPORT_TEMPLATE_STYLESHEETS)
        return raw_source, pdf_source

    def render_sections(self):
        self.context["RENDERED_SECTIONS"] = []
        order = 0
        for section in settings.REPORT_SECTIONS:
            if not section.get("content"):
                # TODO: store html content, but prevent SSTI here!
                self.context["RENDERED_SECTIONS"].append({"template": section["template"]})
                continue
            content_file = os.path.join(settings.REPORT_TEMPLATE_CONTENTS_DIR, section["content"])
            with open(content_file, "r") as f:
                rendered = self._render_markdown_section_context(f.read())
                if not models.ReportSection.objects.filter(report=self.report, name=section["title"]).exists():
                    report_section = models.ReportSection.objects.create(report=self.report, name=section["title"],
                                                                         text=rendered, order=order,
                                                                         project=self.report.project)
                    report_section.template = section["template"]
                    self.context["RENDERED_SECTIONS"].append(report_section)
                    order += 1
                else:
                    report_section = self.report.reportsection_set.get(name=section["title"])
                    report_section.template = section["template"]
                    self.context["RENDERED_SECTIONS"].append(report_section)

    def _render_markdown_section_context(self, content):
        template = engines["django"].from_string(content)
        rendered = template.render(self.context)
        return rendered

    def _markdown_section_to_html(self, content):
        template = engines["django"].from_string(content)
        rendered = template.render(self.context)
        return mark_safe(bleach_md(rendered))
