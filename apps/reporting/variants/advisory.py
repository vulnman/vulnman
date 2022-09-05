import zipfile
import os
from io import BytesIO
from django.template.loader import render_to_string
from apps.reporting.variants.base import Variant


class AdvisoryReport(Variant):
    def __init__(self, report_release, template_name=None, vulnerability=None):
        super().__init__(report_release, template_name=template_name, vulnerability=vulnerability)
        self.template_file = "report_templates/%s/advisory.md" % self.template_name

    def get_context(self):
        context = super().get_context()
        context["vulnerability"] = self.vulnerability
        return context

    def generate_report(self):
        if self.vulnerability.imageproof_set.all():
            s = BytesIO()
            with zipfile.ZipFile(s, "w", zipfile.ZIP_DEFLATED, False) as zip_file:
                raw_source = render_to_string(self.template_file, self.get_context())
                zip_file.writestr("advisory.md", raw_source)
                # export results as zip with proof images
                for image_proof in self.vulnerability.imageproof_set.all():
                    zip_file.write(image_proof.image.path, os.path.basename(image_proof.image.name))
            results = s.getvalue()
            return results, True
        else:
            raw_source = render_to_string(self.template_file, self.get_context())
            return raw_source, False
