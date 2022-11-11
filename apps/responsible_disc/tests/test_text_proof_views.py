from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.responsible_disc import models


class TextProofDeleteViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.vulnerability = self.create_instance(models.Vulnerability, user=self.pentester1)
        self.proof = self.create_instance(models.TextProof, vulnerability=self.vulnerability)
        self.url = self.proof.get_absolute_delete_url()

    def test_valid(self):
        self.client.force_login(self.pentester1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.TextProof.objects.filter(vulnerability=self.vulnerability).count(), 0)

    def test_vendor_unshared(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_pentester2(self):
        self.client.force_login(self.pentester2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_vendor_shared(self):
        # TODO: implement
        pass


class TextProofCreateViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.vulnerability = self.create_instance(models.Vulnerability, user=self.pentester1)
        self.data = {"name": "test", "description": "test1", "text": "test2"}
        self.url = self.get_url("responsible_disc:text-proof-create", pk=self.vulnerability.pk)

    def test_valid(self):
        self.client.force_login(self.pentester1)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.TextProof.objects.filter(vulnerability=self.vulnerability).count(), 1)

    def test_pentester2(self):
        self.client.force_login(self.pentester2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_vendor_shared(self):
        # TODO: implement
        pass

    def test_vendor_unshared(self):
        self.client.force_login(self.vendor)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)
