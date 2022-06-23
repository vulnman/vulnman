from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.responsible_disc.models import Vulnerability
from apps.account import models


class InviteVendorTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vuln1 = self._create_instance(Vulnerability, user=self.pentester1)

    def test_vendor_invite_permissions(self):
        url = self.get_url("responsible_disc:invite-vendor", pk=self.vuln1.pk)
        data = {"email": "testcontact@vendor.com"}
        # unauthorized test
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
        # pentester: allowed
        self.client.force_login(self.pentester1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.User.objects.filter(email=data["email"], is_active=False).count(), 1)
        # vendor: forbidden
        vendor = self._create_user("vendor", "changeme", is_vendor=True)
        self.client.force_login(vendor)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
