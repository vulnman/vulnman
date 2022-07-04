from django.test import TestCase
from vulnman.core.test import VulnmanTestCaseMixin
from apps.account.token import account_activation_token


class ActivateAccountViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_valid_token(self):
        pass
