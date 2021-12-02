from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin


class ProjectDashboardTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_status_code(self):
        self._test_unauth_access("dashboard:dashboard")
