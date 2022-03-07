from django.utils import timezone
from rest_framework.test import APITestCase
from vulnman.api.tests.testcase import VulnmanAPITestCaseMixin
from apps.findings import models
from apps.assets.models import WebApplication


class FindingsViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.forbidden_project = self.create_project()
        self.account1 = self.create_instance(models.UserAccount, project=self.project)
        self.account2 = self.create_instance(models.UserAccount, project=self.forbidden_project)

    def test_useraccount_detail(self):
        url = self.get_url("api:v1:user-account-detail", pk=self.account1.pk)
        self.client.force_login(self.project_pentester)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.denied_pentester)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_useraccount_delete(self):
        url = self.get_url("api:v1:user-account-detail", pk=self.account1.pk)
        self.client.force_login(self.project_pentester)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_useraccount_create(self):
        url = self.get_url("api:v1:user-account-list")
        data = {"username": "testuser", "password": "testpassword", "project": str(self.project.pk)}
        self.client.force_login(self.project_pentester)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        data = {"username": "testuser", "password": "testpassword", "project": str(self.forbidden_project.pk)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_vulnerability_template_list(self):
        self.create_instance(models.Template)
        url = self.get_url("api:v1:vulnerability-template-list")
        self.client.force_login(self.project_pentester)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_proof_detail(self):
        vulnerability = self.create_instance(models.Vulnerability, project=self.project)
        vulnerability2 = self.create_instance(models.Vulnerability, project=self.forbidden_project)
        proof = self.create_instance(models.TextProof, vulnerability=vulnerability)
        url = self.get_url("api:v1:proof-detail", pk=str(proof.pk))
        self.client.force_login(self.project_pentester)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], str(proof.pk))
        self.client.force_login(self.denied_pentester)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_proof_create(self):
        # TODO: implement
        pass

    def test_proof_update(self):
        # TODO: implement
        pass

    def test_vulnerability_detail(self):
        asset = self.create_instance(WebApplication, project=self.project)
        vulnerability = self.create_instance(models.Vulnerability, project=self.project, asset_webapp=asset)
        url = self.get_url("api:v1:vulnerability-detail", pk=str(vulnerability.pk))
        self.client.force_login(self.project_pentester)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.denied_pentester)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_vulnerability_create(self):
        asset = self.create_instance(WebApplication, project=self.project)
        template = self.create_instance(models.Template)
        url = self.get_url("api:v1:vulnerability-list")
        data = {"template": str(template.pk), "name": "My first vuln", "severity": 0, 
            "project": str(self.forbidden_project.pk), "asset_type": WebApplication.ASSET_TYPE, "asset": str(asset.pk)}
        self.client.force_login(self.project_pentester)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        data["project"] = str(self.project.pk)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Vulnerability.objects.filter(project=self.forbidden_project).count(), 0)
        self.assertEqual(models.Vulnerability.objects.filter(project=self.project).count(), 1)
        # test foreign project - asset combination
        not_my_asset = self.create_instance(WebApplication, project=self.forbidden_project)
        data["asset"] = str(not_my_asset.pk)
        data["project"] = str(self.forbidden_project.pk)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(models.Vulnerability.objects.filter(project=self.forbidden_project).count(), 0)