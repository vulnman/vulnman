from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.projects import models


class ProjectListViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:project-list")

    def test_only_my_pentester_projects(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get("projects", [])), 1)
        self.assertEqual(response.context["projects"][0], self.project1)
        # pentester2
        self.client.force_login(self.pentester2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get("projects", [])), 1)
        self.assertEqual(response.context["projects"][0], self.project2)

    def test_no_projects_vendor(self):
        self.client.force_login(self.vendor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_project_status_filter(self):
        self.client.force_login(self.pentester1)
        projects3 = self._create_project(creator=self.pentester1)
        projects3.status = models.Project.PENTEST_STATUS_CLOSED
        projects3.save()
        url = self.url + "?status=%s" % models.Project.PENTEST_STATUS_CLOSED
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get("projects", [])), 1)
        self.assertEqual(response.context["projects"][0], projects3)
