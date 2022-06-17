from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from vulnman.tests.mixins import VulnmanTestMixin
from apps.account import models


class InviteVendorTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    """
    def test_vendor_invite_permissions(self):
        url = self.get_url("account:invite-vendor")
        data = {"email": "testcontact@vendor.com"}
        # unauthorized test
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_URL) + "?next=%s" % url)
        # pentester: allowed
        self.client.force_login(self.pentester1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.InviteCode.objects.filter(token__isnull=False).count(), 1)
        self.assertEqual(models.User.objects.filter(email=data["email"], is_active=False).count(), 1)
        # vendor: forbidden
        vendor = self._create_user("vendor", "changeme", is_vendor=True)
        self.client.force_login(vendor)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
    """
