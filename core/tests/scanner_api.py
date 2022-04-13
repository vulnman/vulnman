from rest_framework.test import APITestCase
from apps.api.v2.mixins import VulnmanAPITestCaseMixin
from apps.findings.models import Vulnerability, TextProof


class TextProofViewSet(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.token1 = self.create_project_token(self.project1, self.pentester1)
        self.token2 = self.create_project_token(self.project2, self.pentester2)

    def test_createview_forbidden_vuln(self):
        """ Test if we can add proofs to
        vulnerabilities not belonging to us
        """

        vuln = self.create_instance(
            Vulnerability, project=self.project1)
        data = {
            "name": "TestProof", "description": "123",
            "vulnerability": str(vuln.pk), "text": "test123"
        }
        url = self.get_url("api:v2:text-proof-list")
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION="Token %s" % self.token2.key)
        self.assertEqual(response.status_code, 400)

    def test_createview(self):
        vuln = self.create_instance(
            Vulnerability, project=self.project1)
        data = {
            "name": "TestProof", "description": "123",
            "vulnerability": str(vuln.pk), "text": "test123"
        }
        url = self.get_url("api:v2:text-proof-list")
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION="Token %s" % self.token1.key)
        self.assertEqual(response.status_code, 201)

    def test_updateview_new_vuln(self):
        """ Check if we can change the vulnerability after creation.
        This should not be allowed.
        """
        vuln = self.create_instance(
            Vulnerability, project=self.project1)
        vuln2 = self.create_instance(
            Vulnerability, project=self.project2
        )
        proof = self.create_instance(TextProof, project=self.project1, vulnerability=vuln)
        data = {"name": "NewTestProof123", "vulnerability": str(vuln2.pk)}
        url = self.get_url("api:v2:text-proof-detail", pk=str(proof.pk))
        self.assertEqual(proof.vulnerability, vuln)
        response = self.client.patch(url, data, HTTP_AUTHORIZATION="Token %s" % self.token1.key)
        self.assertEqual(TextProof.objects.filter(
            vulnerability=vuln).count(), 1)
        self.assertEqual(response.json()["vulnerability"], str(vuln.pk))
