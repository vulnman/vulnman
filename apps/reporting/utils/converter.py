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
        self.render_sections()
        raw_source = render_to_string(self.template.get_template_path(), self.context)
        pdf_source = HTML(string=raw_source).write_pdf(stylesheets=self.template.get_stylesheet_paths())
        return raw_source, pdf_source

    def render_sections(self):
        self.context["RENDERED_SECTIONS"] = []
        self.context["REPORT_TEMPLATE_SECTIONS_DIR"] = self.template.get_sections_directory()
        order = 0
        for section in self.template.get_sections():
            # check if the section has markdown content
            if not section.content_file:
                # TODO: store html only sections in database
                self.context["RENDERED_SECTIONS"].append(
                    {"template": section.get_template_file_path(self.template.get_template_directory())})
                continue
            content = section.get_content(self.template.get_template_directory())
            rendered = self._render_markdown_section_context(content)
            if not models.ReportSection.objects.filter(report=self.report, name=section.title).exists():
                report_section = models.ReportSection.objects.create(report=self.report, name=section.title,
                                                                     text=rendered, order=order,
                                                                     project=self.report.project)
                report_section.template = section.get_template_file_path(self.template.get_template_directory())
                self.context["RENDERED_SECTIONS"].append(report_section)
                order += 1
            else:
                report_section = self.report.reportsection_set.get(name=section.title)
                report_section.template = section.get_template_file_path(self.template.get_template_directory())
                self.context["RENDERED_SECTIONS"].append(report_section)

    def _render_markdown_section_context(self, content):
        template = engines["django"].from_string(content)
        rendered = template.render(self.context)
        return rendered

    def _markdown_section_to_html(self, content):
        template = engines["django"].from_string(content)
        rendered = template.render(self.context)
        return mark_safe(bleach_md(rendered))
