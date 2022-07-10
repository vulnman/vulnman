from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.assets import models


class HostViewsTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.host1 = self._create_instance(models.Host, project=self.project1)
        self.host2 = self._create_instance(models.Host, project=self.project2)

    def test_listview_forbidden(self):
        url = self.get_url("projects:assets:host-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_listview(self):
        url = self.get_url("projects:assets:host-list")
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["hosts"]), 1)

    def test_createview_pentester_role(self):
        url = self.get_url("projects:assets:host-create")
        payload = {"ip": "10.1.4.4", "accessibility": models.Host.ACCESSIBILITY_NOT_ACCESSIBLE}
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)

    def test_createview_readonly_role(self):
        url = self.get_url("projects:assets:host-create")
        payload = {"ip": "10.1.4.4", "accessibility": models.Host.ACCESSIBILITY_NOT_ACCESSIBLE}
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 403)
