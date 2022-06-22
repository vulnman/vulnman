from django.test import TestCase, tag
from django.conf import settings
from django.urls import reverse
from vulnman.tests.mixins import VulnmanTestMixin
from apps.responsible_disc import models
from apps.findings.models import Template


class VulnerabilityListView(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    @tag('not-default')
    def test_listview_forbidden(self):
        url = self.get_url("responsible_disc:vulnerability-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    @tag('not-default')
    def test_listview(self):
        url = self.get_url("responsible_disc:vulnerability-list")
        vuln1 = self._create_instance(models.Vulnerability, user=self.pentester1)
        self._create_instance(models.Vulnerability, user=self.pentester2)
        self.client.force_login(self.pentester1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["vulnerabilities"]), 1)
        self.assertEqual(response.context["vulnerabilities"][0], vuln1)

    @tag('not-default')
    def test_createview(self):
        template = self._create_instance(Template)
        url = self.get_url("responsible_disc:vulnerability-create")
        payload = {"template_id": template.vulnerability_id, "name": "TestVuln",
                   "status": models.Vulnerability.STATUS_OPEN, "vendor": "TestVendor",
                   "vendor_homepage": "https://example.com", "vendor_email": "admin@example.com",
                   "affected_product": "Test Product", "affected_versions": "<1.0.0",
                   "severity": ""
                   }
        self.client.force_login(self.pentester1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Vulnerability.objects.count(), 1)

    @tag('not-default')
    def test_detail_view(self):
        vuln = self._create_instance(models.Vulnerability, user=self.pentester1)
        url = self.get_url("responsible_disc:vulnerability-detail", pk=vuln.pk)
        self.client.force_login(self.pentester1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @tag('not-default')
    def test_detail_view_forbidden(self):
        vuln = self._create_instance(models.Vulnerability, user=self.pentester1)
        url = self.get_url("responsible_disc:vulnerability-detail", pk=vuln.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_URL) + "?next=" + url)

    @tag('not-default')
    def test_vuln_create_vendor(self):
        template = self._create_instance(Template)
        url = self.get_url("responsible_disc:vulnerability-create")
        payload = {"template_id": template.vulnerability_id, "name": "TestVuln",
                   "status": models.Vulnerability.STATUS_OPEN, "vendor": "TestVendor",
                   "vendor_homepage": "https://example.com", "vendor_email": "admin@example.com",
                   "affected_product": "Test Product", "affected_versions": "<1.0.0",
                   "severity": ""
                   }
        vendor = self._create_user("vendor", "changeme", is_vendor=True)
        self.client.force_login(vendor)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(models.Vulnerability.objects.count(), 0)


class TextProofViewsTextCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    @tag('not-default')
    def test_text_proof_create(self):
        vulnerability = self._create_instance(models.Vulnerability, user=self.pentester1)
        url = self.get_url("responsible_disc:text-proof-create", pk=vulnerability.pk)
        data = {"name": "test", "description": "lorem", "text": "ipsum"}
        # unauth
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
        # permission denied
        self.client.force_login(self.pentester2)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
        # allowed
        self.client.force_login(self.pentester1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
