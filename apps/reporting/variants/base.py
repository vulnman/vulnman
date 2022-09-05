from apps.findings.models import Vulnerability


class Variant(object):

    def __init__(self, report_release, template_name=None, vulnerability=None):
        self.report_release = report_release
        self.template_name = template_name
        if not template_name:
            self.template_name = report_release.report.template
        if self.report_release:
            self.project = self.report_release.project
        else:
            try:
                self.project = vulnerability.project
            except Exception:
                self.project = None
        self.vulnerability = vulnerability

    def get_vulnerabilities_by_severity(self, severity):
        return self.project.vulnerability_set.filter(severity=severity, status=Vulnerability.STATUS_OPEN)

    def get_critical_severity_vulnerabilities(self):
        return self.get_vulnerabilities_by_severity(4)

    def get_high_severity_vulnerabilities(self):
        return self.get_vulnerabilities_by_severity(3)

    def get_medium_severity_vulnerabilities(self):
        return self.get_vulnerabilities_by_severity(2)

    def get_low_severity_vulnerabilities(self):
        return self.get_vulnerabilities_by_severity(1)

    def get_informational_severity_vulnerabilities(self):
        return self.get_vulnerabilities_by_severity(0)

    def get_context(self):
        context = {"release": self.report_release, "project": self.project, "variant": self}
        return context

    def generate_report(self):
        raise NotImplementedError

    def generate(self):
        raw_source, compiled_source = self.generate_report()
        self.report_release.raw_source = raw_source
        self.report_release.compiled_source = compiled_source
        self.report_release.task_id = None
        self.report_release.save()
        return True, "Report Release created!"
