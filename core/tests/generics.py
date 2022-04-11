from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.findings.models import Vulnerability


class ProjectListView(TestCase, VulnmanTestMixin):
    def setUp(self):
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("projects:findings:vulnerability-list")
        self.login_with_project(self.pentester1, self.project1)
        vuln = self._create_instance(Vulnerability, project=self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["vulns"][0], vuln)

    def test_listview_forbidden(self):
        # Even if pentester2 is able to get to login with project1
        # check permission denied is still active
        url = self.get_url("projects:findings:vulnerability-list")
        self.login_with_project(self.pentester2, self.project1)
        vuln = self._create_instance(Vulnerability, project=self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
