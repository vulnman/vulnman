from django.utils import timezone
from rest_framework.test import APITestCase
from vulnman.core.test import VulnmanAPITestCaseMixin
from apps.projects import models


class ProjectAPITokenTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_token_expired(self):
        date_valid = timezone.now() + timezone.timedelta(days=3)
        token = self.create_instance(models.ProjectAPIToken, project=self.project1, date_valid=date_valid)
        url = self.get_url("api:v1:assets:host-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        response = self.client.get(url, HTTP_AUTHORIZATION="Token %s" % token.key)
        self.assertEqual(response.status_code, 200)
        date_valid = timezone.now() - timezone.timedelta(days=3)
        token = self.create_instance(models.ProjectAPIToken, project=self.project1, date_valid=date_valid)
        response = self.client.get(url, HTTP_AUTHORIZATION="Token %s" % token.key)
        self.assertEqual(response.status_code, 401)
        self.assertEqual("expired" in response.json().get("detail"), True)
