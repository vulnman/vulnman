from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin


class PasswordChangeViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_change_password(self):
        url = self.get_url("account:change-password")
        data = {"old_password": "changeme",
                "new_password1": "changeme1234", "new_password2": "changeme1234"}
        self.client.force_login(self.pentester1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
