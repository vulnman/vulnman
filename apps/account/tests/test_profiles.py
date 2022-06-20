from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from vulnman.tests.mixins import VulnmanTestMixin
from apps.account import models


class UpdateProfileViewsTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_public_profile(self):
        self.pentester1.pentester_profile.is_public = True
        self.pentester1.pentester_profile.save()
        url = self.get_url("account:user-profile", slug=self.pentester1.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.pentester1.pentester_profile.is_public = False
        self.pentester1.pentester_profile.save()
        response = self.client.get(url)
        self.assertEqual(b"This profile is not public" in response.content, True)

    def test_update_profile(self):
        url = self.get_url("account:profile-update")
        data = {"first_name": "Test", "last_name": "lorem", "is_public": True,
                "public_real_name": True, "public_email_address": True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_URL) + "?next=" + url)
