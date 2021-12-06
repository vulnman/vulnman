from rest_framework.test import APITestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.methodologies import models


class MethodologyAPITestCase(APITestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("api:methodologies:methodology-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # try logged in
        self.client.force_login(self.user1)
        obj = self._create_instance(models.Methodology)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(obj.pk))
