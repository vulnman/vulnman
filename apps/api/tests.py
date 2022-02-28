from django.test import TestCase
from django.contrib.auth.models import User


class SimpleAPITest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("jdoe", password="change")

    def test_vulnerability_template_autocomplete(self):
        url = '/vulnerability-templates/autocomplete/?q=sql'
        response = self.client.get(url)
        # check redirect to login
        self.assertEqual(response.status_code, 302)
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
