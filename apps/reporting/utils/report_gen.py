import os
import sass
import weasyprint
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from django.conf import settings


class ReportGenerator(object):
    def __init__(self, template_name):
        self.template_name = template_name
        self.template_root_path = os.path.join(
            settings.BASE_DIR, "resources/report_templates/{template}".format(template=template_name)
        )

    def get_stylesheets(self):
        css_paths = []
        report_root_path = os.path.join(settings.BASE_DIR, "resources/templates/report_templates/{template}".format(
            template=self.template_name))
        css_list = settings.REPORT_TEMPLATES.get(self.template_name).get("CSS", [])
        for css in css_list:
            new_css_path = os.path.join(report_root_path, css)
            css_paths.append(
                new_css_path
            )
        # append sass files
        sass_path = os.path.join(report_root_path, "scss/main.scss")
        if os.path.exists(sass_path):
            compiled_scss = sass.compile(filename=sass_path, output_style="compressed")
            css_paths.append(CSS(string=compiled_scss))
        return css_paths

    def url_fetcher(self, url, *args, **kwargs):
        # strip "../" using basename
        report_template = os.path.basename(self.template_name)
        report_root_path = os.path.join(settings.BASE_DIR, "resources/templates/report_templates/{template}".format(
            template=report_template))
        if url.startswith('file:'):
            media_name = url.replace("file://", "")
            media_path = os.path.join(report_root_path, media_name)
            return dict(file_obj=open(media_path, "rb"))

        return weasyprint.default_url_fetcher(url, *args, **kwargs)

    def generate(self, raw_source):
        font_config = FontConfiguration()
        compiled_source = HTML(string=raw_source, url_fetcher=self.url_fetcher).write_pdf(
            stylesheets=self.get_stylesheets(),
            font_config=font_config)
        return compiled_source
