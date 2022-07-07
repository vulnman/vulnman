from django.test import TestCase
from django.utils import timezone
from vulnman.core.test import VulnmanTestCaseMixin
from apps.projects import models


class ProjectCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:project-create")
        self.customer = self._create_instance(models.Client)

    def test_create_pentester(self):
        data = {"name": "Test Project Lorem", "start_date": timezone.now().date(),
                "end_date": timezone.now().date(), "client": self.customer.pk, "cvss_required": False,
                "pentest_method": models.Project.PENTEST_METHOD_WHITEBOX}
        self.client.force_login(self.pentester1)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Project.objects.filter(name=data["name"]).count(), 1)

    def test_create_unauthenticated(self):
        data = {"name": "Test Project Lorem", "start_date": timezone.now().date(),
                "end_date": timezone.now().date(), "client": self.customer.pk, "cvss_required": False,
                "pentest_method": models.Project.PENTEST_METHOD_WHITEBOX}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 403)

    def test_create_vendor(self):
        data = {"name": "Test Project Lorem", "start_date": timezone.now().date(),
                "end_date": timezone.now().date(), "client": self.customer.pk, "cvss_required": False,
                "pentest_method": models.Project.PENTEST_METHOD_WHITEBOX}
        self.client.force_login(self.vendor)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 403)
