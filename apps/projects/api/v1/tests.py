from rest_framework.test import APITestCase
from vulnman.tests.mixins import VulnmanAPITestMixin
from apps.projects import models


class ProjectViewSetTest(APITestCase, VulnmanAPITestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("api:v1:project-list")
        self.client.force_login(self.user1)
        project = self._create_project(creator=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(project.pk))
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)

    def test_detailview(self):
        project = self._create_project(creator=self.user1)
        url = self.get_url("api:v1:project-detail", pk=project.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], str(project.pk))
"""
    def test_createview(self):
        url = self.get_url("api:v1:project-list")
        client = self._create_instance(models.Client)
        self.client.force_login(self.user1)
        payload = {"client": str(client.name), "start_date": client.date_created.date(),
                   "end_date": client.date_created.date()}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Project.objects.filter(creator=self.user1).count(), 1)
        self.client.logout()
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 403)
"""
