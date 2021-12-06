from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin


class ProjectDashboardTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_status_code(self):
        url = self.get_url("dashboard:dashboard")
        self._test_unauthenticated_aceess(url, expected_status_code=200)
