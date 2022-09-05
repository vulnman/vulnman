import io
from apps.reporting.variants.base import Variant


class CSVReport(Variant):
    # Generate a csv report
    def __init__(self, report_release, template_name=None, vulnerability=None):
        super().__init__(report_release, template_name=template_name, vulnerability=vulnerability)
        self.output = io.StringIO()
