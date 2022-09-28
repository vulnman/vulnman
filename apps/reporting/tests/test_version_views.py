from django.test import TestCase
from django.utils import timezone
from vulnman.core.test import VulnmanTestCaseMixin
from apps.reporting import models


class VersionUpdateViewTestcase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(models.Report, project=self.project1)
        self.report2 = self.create_instance(models.Report, project=self.project2)
        self.version1 = self.create_instance(models.ReportVersion, report=self.report1, project=self.project1,
                                             change=models.ReportVersion.REPORT_CHANGE_REPORT_CREATED)
        self.version2 = self.create_instance(models.ReportVersion, report=self.report2, project=self.project2)
        self.url1 = self.get_url("projects:reporting:version-update", pk=self.version1.pk)
        self.url2 = self.get_url("projects:reporting:version-update", pk=self.version2.pk)
        self.data = {"change": models.ReportVersion.REPORT_CHANGE_REPORT_FINALIZED, "version": 0.2,
                     "user": self.pentester1.pk, "date": timezone.now().date()}

    def test_status_code(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url1, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.ReportVersion.objects.filter(change=models.ReportVersion.REPORT_CHANGE_REPORT_FINALIZED,
                                                             pk=self.version1.pk).count(), 1)

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url1, data=self.data)
        self.assertEqual(response.status_code, 403)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url1, data=self.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.ReportVersion.objects.filter(change=models.ReportVersion.REPORT_CHANGE_REPORT_FINALIZED,
                                                             pk=self.version1.pk).count(), 0)

    def test_any_user(self):
        self.data["user"] = self.pentester2.pk
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url1, data=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context.get("form"))
        self.assertIsNotNone(response.context["form"].errors)
