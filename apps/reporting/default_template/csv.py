import csv
from apps.reporting.variants import CSVReport
from apps.findings.models import Vulnerability


class Report(CSVReport):
    def __init__(self, report_release, template_name=None, vulnerability=None):
        super().__init__(report_release, template_name=template_name, vulnerability=vulnerability)

    def get_vulnerabilities_open(self):
        return self.project.vulnerability_set.filter(status=Vulnerability.STATUS_OPEN)

    def get_vulnerabilities_fixed(self):
        return self.project.vulnerability_set.filter(status=Vulnerability.STATUS_FIXED)

    def generate_report(self):
        header = ["Name", "Vulnerability Type", "Severity", "Category", "Component"]
        writer = csv.writer(self.output)
        writer.writerow(header)
        for vuln in self.get_vulnerabilities_open():
            data = [vuln.name, vuln.template.name, vuln.get_severity_display(), vuln.template.category,
                    vuln.asset.name]
            writer.writerow(data)
        return self.output.getvalue(), self.output.getvalue().encode()
