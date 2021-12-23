from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.findings import models


class TemplateTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("findings:template-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        template = self._create_instance(models.Template)
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data["vuln_templates"]), 1)
        self.assertEqual(response.context_data["vuln_templates"][0].pk, template.pk)

    def test_creatview(self):
        url = self.get_url("findings:template-create")
        payload = {"name": "test vulnerability", "description": "lorem ipsum", "resolution": "fix it",
                   "ease_of_resolution": "undetermined", "reference_set-TOTAL_FORMS": "1", "reference_set-0-uuid": "",
                   "reference_set-0-template": "",
                   "reference_set-0-name": "CWE-1234", "reference_set-0-DELETE": "",
                   "reference_set-MAX_NUM_FORMS": "4",
                   "reference_set-INITIAL_FORMS": "0", "reference_set-MIN_NUM_FORMS": "0"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Template.objects.count(), 0)
        self.client.force_login(self.user1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Template.objects.count(), 1)
        self.assertEqual(models.Reference.objects.count(), 1)
        self.assertEqual(models.Template.objects.filter(name="test vulnerability").count(), 1)
        self.assertEqual(models.Template.objects.filter(creator=self.user1).count(), 1)

    def test_updateview(self):
        template = self._create_instance(models.Template, name="before")
        url = self.get_url("findings:template-update", pk=template.pk)
        payload = {"name": "after", "description": "lorem ipsum", "resolution": "fix it",
                   "ease_of_resolution": "undetermined"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Template.objects.filter(name="after").count(), 0)
        self.client.force_login(self.user1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Template.objects.filter(name="after").count(), 1)


class VulnerabilityTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("projects:findings:vulnerability-list")
        vulnerability = self._create_instance(models.Vulnerability, project__creator=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.login_with_project(self.user1, self.user1.project_set.first())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data["vulns"]), 1)
        self.assertEqual(response.context_data["vulns"][0].pk, vulnerability.pk)

    def test_detailview(self):
        vulnerability = self._create_instance(models.Vulnerability, project__creator=self.user1)
        url = self.get_url("projects:findings:vulnerability-detail", pk=vulnerability.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.login_with_project(self.user1, self.user1.project_set.first())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["vuln"].pk, vulnerability.pk)
        self.client.force_login(self.user2)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_deleteview(self):
        vulnerability = self._create_instance(models.Vulnerability, project__creator=self.user1)
        url = self.get_url("projects:findings:vulnerability-delete", pk=vulnerability.pk)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Vulnerability.objects.count(), 1)
        self.login_with_project(self.user1, self.user1.project_set.first())
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Vulnerability.objects.count(), 0)

    def test_createview(self):
        url = self.get_url("findings:vulnerability-create")
        # payload = {}