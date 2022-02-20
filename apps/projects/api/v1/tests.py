from django.utils import timezone
from rest_framework.test import APITestCase
from vulnman.api.tests.testcase import VulnmanAPITestCaseMixin
from apps.projects import models


class ProjectViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.forbidden_project = self.create_instance(models.Project)

    def test_listview(self):
        url = self.get_url("api:v1:project-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.project_pentester)
        response = self.client.get(url)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(self.project.pk))

    def test_detailview(self):
        url = self.get_url("api:v1:project-detail", pk=self.project.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.project_pentester)
        response = self.client.get(url)
        self.assertEqual(response.json()["uuid"], str(self.project.pk))

    def test_createview(self):
        url = self.get_url("api:v1:project-list")
        client = self.create_instance(models.Client)
        data = {"name": "Test Project", "start_date": timezone.now().date(), "end_date": timezone.now().date(), "client": str(client.pk)}
        self.client.force_login(self.project_pentester)
        response = self.client.post(url, data)
        self.assertEqual(models.Project.objects.filter(name="Test Project").count(), 1)
        url = self.get_url("api:v1:project-detail", pk=response.json()["uuid"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.denied_pentester)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
