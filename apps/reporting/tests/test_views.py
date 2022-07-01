from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.reporting import models


class ReportViewTestcase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_report_list(self):
        report = self._create_instance(models.Report, project=self.project1)
        url = self.get_url("projects:reporting:report-list")
        # forbidden - empty reports list for other user
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get("reports", [])), 0)
        # allowed
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get("reports", [])), 1)
        self.assertEqual(response.context["reports"][0], report)

    def test_report_create(self):
        url = self.get_url("projects:reporting:report-create")
        payload = {"author": self.pentester1.pk, "title": "", "language": "de", "name": "Test", "template": "default"}
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Report.objects.filter(project=self.project1, author=self.pentester1,
                                                      template="default", language="de").count(), 1)

    def test_report_detail(self):
        report = self._create_instance(models.Report, project=self.project1)
        url = self.get_url("projects:reporting:report-detail", pk=report.pk)
        # forbidden
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # allowed
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["report"].pk, report.pk)
