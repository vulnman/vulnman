from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.findings import models
from apps.assets.models import WebApplication


class VulnerabilityListViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:findings:vulnerability-list")
        self.vulnerability = self._create_instance(models.Vulnerability, project=self.project1)

    def test_pentester1(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["vulns"]), 1)

    def test_pentester2(self):
        self.login_with_project(self.pentester2, self.project2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["vulns"]), 0)

    def test_readonly(self):
        pass


class VulnerabilityCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("projects:findings:vulnerability-create")
        self.template = self._create_instance(models.Template)
        self.asset1 = self._create_instance(models.WebApplication, project=self.project1)
        self.asset2 = self._create_instance(models.WebApplication, project=self.project2)
        self.data = {"name": "Testvuln", "template_id": self.template.vulnerability_id,
                     "f_asset": self.asset1.pk, "status": models.Vulnerability.STATUS_OPEN, "auth_required": True,
                     "user_account": "", "asset_type": models.WebApplication.ASSET_TYPE}

    def test_pentester1(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Vulnerability.objects.filter(template=self.template,
                                                             asset_webapp=self.asset1).count(), 1)

    def test_pentester2(self):
        pass

    def test_readonly(self):
        self.login_with_project(self.read_only1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_asset_other_project(self):
        self.data["f_asset"] = self.asset2.pk
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["form"].errors), 1)
        self.assertEqual(models.Vulnerability.objects.filter(template=self.template, project=self.project1,
                                                             asset_webapp=self.asset1).count(), 0)


class AddTextProofViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vulnerability = self._create_instance(models.Vulnerability, project=self.project1)
        self.url = self.get_url("projects:findings:vulnerability-add-text-proof", pk=self.vulnerability.pk)
        self.data = {"name": "lorem", "description": "myproof", "text": "sometext"}

    def test_pentester1(self):
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.TextProof.objects.filter(project=self.project1,
                                                         vulnerability=self.vulnerability).count(), 1)

    def test_pentester2(self):
        pass

    def test_readonly(self):
        pass

    def test_other_vulnerability(self):
        pass
