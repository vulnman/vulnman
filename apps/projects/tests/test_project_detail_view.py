from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin


class ProjectDetailTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_my_project(self):
        url = self.get_url("projects:project-detail", pk=self.project1.pk)
        self.client.force_login(self.pentester1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("project"), self.project1)

    def test_other_project_priv_esc(self):
        url = self.get_url("projects:project-detail", pk=self.project2.pk)
        self.client.force_login(self.pentester1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.context.get("project"), None)

    def test_project_vendor(self):
        url = self.get_url("projects:project-detail", pk=self.project1.pk)
        self.client.force_login(self.vendor)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
