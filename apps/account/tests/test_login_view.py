from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from vulnman.core.test import VulnmanTestCaseMixin
from apps.account.models import User


class LoginViewBaseTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.url = self.get_url("account:login")

    def test_login_pentester(self):
        data = {"auth-username": self.pentester1.username,
                "auth-password": "changeme", "login-current_step": "auth"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_login_vendor(self):
        vendor = self._create_user("testvendor", "password", user_role=User.USER_ROLE_VENDOR)
        data = {"auth-username": vendor.username, "auth-password": "password", "login-current_step": "auth"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_login_wrong_creds(self):
        data = {"auth-username": "randomusername", "auth-password": "randompassword", "login-current_step": "auth"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('form').is_valid(), False)
