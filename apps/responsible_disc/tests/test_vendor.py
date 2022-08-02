from django.test import TestCase
from guardian.shortcuts import get_user_perms
from vulnman.core.test import VulnmanTestCaseMixin
from apps.responsible_disc.models import Vulnerability
from apps.account import models


class InviteVendorTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.vuln1 = self._create_instance(Vulnerability, user=self.pentester1)

    def test_vendor_invite_permissions(self):
        url = self.get_url("responsible_disc:invite-vendor", pk=self.vuln1.pk)
        data = {"email": "testcontact@vendor.com"}
        # unauthorized test
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
        # vendor: forbidden
        vendor = self._create_user("vendor", "changeme", is_vendor=True)
        self.client.force_login(vendor)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
        # pentester: allowed
        self.client.force_login(self.pentester1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.User.objects.filter(email=data["email"], is_active=False, is_vendor=True).count(), 1)
        user = models.User.objects.get(email=data["email"])
        self.assertEqual(len(get_user_perms(user, self.vuln1)), 2)
        self.assertIn("view_vulnerability", get_user_perms(user, self.vuln1))
        self.assertIn("add_comment", get_user_perms(user, self.vuln1))
        # pentester2: forbidden
        self.client.force_login(self.pentester2)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_share_vuln_existing_user(self):
        url = self.get_url("responsible_disc:invite-vendor", pk=self.vuln1.pk)
        data = {"email": self.pentester2.email}
        self.client.force_login(self.pentester1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(get_user_perms(self.pentester2, self.vuln1)), 2)
