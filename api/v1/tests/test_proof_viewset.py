from rest_framework.test import APITestCase
from api.v1.mixins import VulnmanAPITestCaseMixin
from apps.findings import models
from apps.projects.models import ProjectContributor


class ProofViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def dtest_forbidden_create_method(self):
        url = self.get_url("api:v1:vulnerability-proof-list")
        payload = {"data": "lorem"}
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 405)

    def test_forbidden_delete_method(self):
        obj = self.create_instance(models.TextProof)
        url = self.get_url("api:v1:vulnerability-proof-detail", pk=str(obj.pk))
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)

    def test_forbidden_retrieve_method(self):
        obj = self.create_instance(models.TextProof)
        url = self.get_url("api:v1:vulnerability-proof-detail", pk=str(obj.pk))
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_updateview(self):
        vuln = self.create_instance(models.Vulnerability, project=self.project1)
        proof1 = self.create_instance(models.TextProof, vulnerability=vuln)
        proof2 = self.create_instance(models.ImageProof, vulnerability=vuln)
        url = self.get_url("api:v1:vulnerability-proof-detail", pk=str(proof1.pk))
        self.login_with_project(self.pentester1, self.project1)
        data = {"order": "1", "pk": str(proof1.pk)}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("order"), 1)
        self.assertEqual(models.TextProof.objects.filter(order=1).count(), 1)
        url = self.get_url("api:v1:vulnerability-proof-detail", pk=str(proof2.pk))
        data = {"order": 2, "pk": str(proof2.pk)}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("order"), 2)

    def test_read_only_forbidden(self):
        vuln = self.create_instance(models.Vulnerability, project=self.project1)
        proof1 = self.create_instance(models.TextProof, vulnerability=vuln)
        self.create_instance(models.ImageProof, vulnerability=vuln)
        self.add_contributor(self.pentester2, project=self.project1, role=ProjectContributor.ROLE_READ_ONLY)
        from guardian.shortcuts import get_user_perms
        print(get_user_perms(self.pentester2, self.project1))
        url = self.get_url("api:v1:vulnerability-proof-detail", pk=str(proof1.pk))
        self.login_with_project(self.pentester2, self.project1)
        data = {"order": "1", "pk": str(proof1.pk)}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 403)
