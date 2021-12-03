from vulnman.tests.mixins import VulnmanTestMixin
from rest_framework import status
from rest_framework.test import APITestCase
from apps.projects import models
from apps.projects.api import serializers


class ProjectAPITestCase(APITestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_unauth_read_access(self):
        urls = ["api:projects:project-list"]
        for url in urls:
            response = self.client.get(self.get_url(url))
            self.assertEqual(response.status_code, 403)

    def test_project_list(self):
        self.client.force_login(self.user1)
        url = self.get_url('api:projects:project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test other users project is hidden from us
        self._create_project("testproject", creator=self.user2)
        response = self.client.get(url)
        self.assertEqual(models.Project.objects.count(), 1)
        self.assertEqual(response.data, [])
        # test if we see our project
        project = self._create_project("myproject", creator=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0], serializers.ProjectSerializer(project).data)

    def test_project_create(self):
        url = self.get_url("api:projects:project-list")
        payload = {'customer': 'testcasecustomer', "name": "testcaseproject"}
        # try create project without authentication
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 403)
        # try create project with authentication
        self.client.force_login(self.user1)
        _response = self.client.post(url, payload)
        self.assertEqual(models.Project.objects.count(), 1)
        self.assertEqual(models.Project.objects.filter(creator=self.user1).count(), 1)

    def test_project_receive(self):
        project = self._create_project("testcaseproject", creator=self.user1)
        url = self.get_url("api:projects:project-detail", pk=project.pk)
        # try receive project detail without auth
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # receive project detail with auth
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), serializers.ProjectSerializer(project).data)
        # receive project from other user
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
