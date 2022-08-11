from rest_framework.test import APITestCase
from vulnman.core.test import VulnmanAPITestCaseMixin
from apps.assets.models import WebApplication, Host
from apps.findings import models


class VulnerabilityViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.template = self.create_instance(models.Template)
        self.host1 = self.create_instance(Host, project=self.project1)
        self.host2 = self.create_instance(Host, project=self.project2)
        self.data = {"name": "test", "template_id": self.template.vulnerability_id,
                     "severity": 0, "asset": self.host1.pk}

    def test_create_view(self):
        url = self.get_url("api:v1:findings:vulnerability-list")
        response = self.post(url, self.data, self.token1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Vulnerability.objects.first().template, self.template)

    def test_create_view_forbidden(self):
        url = self.get_url("api:v1:findings:vulnerability-list")
        response = self.post(url, self.data, self.token2)
        self.assertEqual(response.status_code, 400)


class TextProofViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vulnerability1 = self.create_instance(models.Vulnerability, project=self.project1)
        self.vulnerability2 = self.create_instance(models.Vulnerability, project=self.project2)
        self.data = {"text": "1234", "name": "My Proof", "description": "123", "vulnerability": self.vulnerability1.pk}

    def test_create_view(self):
        url = self.get_url("api:v1:findings:text-proof-list")
        response = self.post(url, self.data, self.token1)
        self.assertEqual(response.status_code, 201)

    def test_create_view_foreign_vuln(self):
        url = self.get_url("api:v1:findings:text-proof-list")
        self.data["vulnerability"] = self.vulnerability2.pk
        response = self.post(url, self.data, self.token1)
        self.assertEqual(response.status_code, 400)

    def test_list_view(self):
        proof1 = self.create_instance(models.TextProof, vulnerability=self.vulnerability1)
        proof2 = self.create_instance(models.TextProof, vulnerability=self.vulnerability2)
        url = self.get_url("api:v1:findings:text-proof-list")
        response = self.get(url, self.token1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(proof1.pk))