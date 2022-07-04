from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin


class SecurityHeadersTestCase(TestCase, VulnmanTestMixin):
    def test_clickjacking(self):
        url = self.get_url("index")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")
