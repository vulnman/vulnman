from django.test import TestCase
from django.utils import timezone
from vulnman.core.test import VulnmanTestCaseMixin
from apps.projects import models


class ProjectUpdateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.customer = self._create_instance(models.Client)

    def test_pentester(self):
        url = self.get_url("projects:project-update", pk=self.project1.pk)
        data = {"name": "Test Project Lorem", "start_date": timezone.now().date(),
                "end_date": timezone.now().date(), "client": self.customer.pk, "cvss_required": False,
                "pentest_method": models.Project.PENTEST_METHOD_WHITEBOX}
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Project.objects.filter(name=data["name"]).count(), 1)

    def test_unauthenticated(self):
        url = self.get_url("projects:project-update", pk=self.project1.pk)
        data = {"name": "Test Project Lorem"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_pentester_broken_access(self):
        url = self.get_url("projects:project-update", pk=self.project1.pk)
        data = {"name": "Test Project Lorem", "start_date": timezone.now().date(),
                "end_date": timezone.now().date(), "client": self.customer.pk, "cvss_required": False,
                "pentest_method": models.Project.PENTEST_METHOD_WHITEBOX}
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.Project.objects.filter(name=data["name"], pk=self.project1.pk).count(), 0)

    def test_vendor_priv_esc(self):
        url = self.get_url("projects:project-update", pk=self.project1.pk)
        data = {"name": "lorem ipsum"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)


class ProjectUpdateCloseViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:project-close", pk=self.project1.pk)

    def test_valid(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Project.objects.filter(status=models.Project.PENTEST_STATUS_CLOSED).count(), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Project.objects.filter(status=models.Project.PENTEST_STATUS_CLOSED,
                                                       pk=self.project1.pk).count(), 0)
