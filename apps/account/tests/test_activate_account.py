from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.account.token import account_activation_token
from django.utils.http import urlsafe_base64_encode
from apps.account.models import User


class ActivateAccountViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_valid_token(self):
        user1 = self._create_user("testvendor", "changeme", user_role=User.USER_ROLE_VENDOR, is_active=False)
        token = account_activation_token.make_token(user1)
        uidb64 = urlsafe_base64_encode(str(user1.pk).encode())
        url = self.get_url("account:activate-account", token=token, uidb64=uidb64)
        data = {"new_password1": "changeme1234!", "new_password2": "changeme1234!", "submit": "Activate"}
        response = self.client.get(url, follow=True)
        new_url = response.redirect_chain[-1][0]
        response = self.client.post(new_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(pk=user1.pk, is_active=True).count(), 1)
