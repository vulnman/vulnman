from rest_framework.test import APITestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.methodologies import models


class MethodologyAPITestCase(APITestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("api:v1:methodology-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # try logged in
        self.client.force_login(self.user1)
        obj = self._create_instance(models.Methodology)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(obj.pk))

    def test_createview(self):
        url = self.get_url("api:v1:methodology-list")
        payload = {"tasks": [
            {"name": "testtask", "description": "testtask description"}], "name": "test1", "description": "test"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user1)
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Methodology.objects.count(), 1)
        self.assertEqual(models.Task.objects.count(), 1)
        self.assertEqual(models.Methodology.objects.first().task_set.count(), 1)

    def test_detailview(self):
        pass

    def test_deleteview(self):
        pass
