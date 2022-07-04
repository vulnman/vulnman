from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from vulnman.core.test import VulnmanTestCaseMixin


class IndexViewTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_status_code(self):
        url = self.get_url("index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_URL))

    def test_redirect_logged_in(self):
        url = self.get_url("index")
        self.client.force_login(self.pentester1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
