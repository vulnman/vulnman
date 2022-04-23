from rest_framework.test import APITestCase
from api.v1.mixins import VulnmanAPITestCaseMixin
from apps.assets import models


class SessionHostViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_listview(self):
        host1 = self.create_instance(models.Host, project=self.project1)
        self.create_instance(models.Host, project=self.project2)
        url = self.get_url("api:v1:host-list")
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(host1.pk))
