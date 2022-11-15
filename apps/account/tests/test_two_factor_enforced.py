from django.test import TestCase
from django.conf import settings
from vulnman.core.test import VulnmanTestCaseMixin


class TwoFactorEnforcedTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        settings.TOTP_ENFORCE_2FA = True
        self.url = self.get_url("projects:project-list")

    def test_redirect_to_setup_page(self):
        self.client.force_login(self.pentester1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.get_url("account:setup-2fa") + "?next=/projects/")
