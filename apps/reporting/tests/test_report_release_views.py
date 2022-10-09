from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.reporting import models


class ReportReleaseListViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(models.Report, project=self.project1)
        self.release1 = self.create_instance(models.ReportRelease, report=self.report1, project=self.project1)
        self.report2 = self.create_instance(models.Report, project=self.project2)
        self.release2 = self.create_instance(models.ReportRelease, report=self.report2, project=self.project2)
        self.url = self.get_url("projects:reporting:report-release-list", pk=self.report1.pk)

    def test_status_code(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["releases"]), 1)
        self.assertEqual(response.context["releases"][0], self.release1)

    def test_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class ReportReleaseDeleteView(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(models.Report, project=self.project1)
        self.release1 = self.create_instance(models.ReportRelease, report=self.report1, project=self.project1)
        self.report2 = self.create_instance(models.Report, project=self.project2)
        self.release2 = self.create_instance(models.ReportRelease, report=self.report2, project=self.project2)

    def test_status_code(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.release1.get_absolute_delete_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.ReportRelease.objects.filter(pk=self.release1.pk).count(), 0)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.release1.get_absolute_delete_url())
        self.assertEqual(response.status_code, 404)

    def test_read_only(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.release1.get_absolute_delete_url())
        self.assertEqual(response.status_code, 403)


class ReportReleaseDetailView(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.report1 = self.create_instance(models.Report, project=self.project1)
        self.release1 = self.create_instance(models.ReportRelease, report=self.report1, project=self.project1)
        self.report2 = self.create_instance(models.Report, project=self.project2)
        self.release2 = self.create_instance(models.ReportRelease, report=self.report2, project=self.project2)

    def test_status_code(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(self.release1.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.get(self.release1.get_absolute_url())
        self.assertEqual(response.status_code, 404)
