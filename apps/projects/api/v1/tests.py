from django.utils import timezone
from rest_framework.test import APITestCase
from vulnman.api.tests.testcase import VulnmanAPITestCaseMixin
from apps.projects import models


class ProjectViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.forbidden_project = self.create_instance(models.Project, creator=self.denied_pentester)

    def test_listview(self):
        url = self.get_url("api:v1:project-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        self.client.force_login(self.project_pentester)
        response = self.client.get(url)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(self.project.pk))

    def test_detailview(self):
        url = self.get_url("api:v1:project-detail", pk=self.project.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        self.client.force_login(self.project_pentester)
        response = self.client.get(url)
        self.assertEqual(response.json()["uuid"], str(self.project.pk))

    def ftest_createview(self):
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

    def test_archive_project(self):
        url = self.get_url("api:v1:project-archive-project", pk=str(self.project.pk))
        data = {"is_archived": True}
        self.client.force_login(self.denied_pentester)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 404)
        self.client.force_login(self.project_pentester)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Project.objects.filter(is_archived=True).count(), 1)
        # test create obj for archived project
        data = {"name": "Test Web Application", "base_url": "https://example.com", "description": "Test", "in_pentest_project": True, "project": str(self.project.pk)}
        url = self.get_url("api:v1:webapplication-list")
        self.client.force_login(self.project_pentester)
        response = self.client.post(url, data)
        self.assertEqual(self.project.webapplication_set.count(), 0)


class ProjectContributorViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.forbidden_project = self.create_instance(models.Project)

    def test_create(self):
        url = self.get_url("api:v1:project-contributor-list")
        data = {"role": models.ProjectContributor.ROLE_PENTESTER, "user": str(self.denied_pentester.username), "project": str(self.project.pk)}
        self.client.force_login(self.denied_pentester)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(models.ProjectContributor.objects.filter(user=self.denied_pentester, project=self.project).count(), 0)
        self.client.force_login(self.project_pentester)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.ProjectContributor.objects.filter(user=self.denied_pentester, project=self.project).count(), 1)
        self.assertEqual(self.denied_pentester.has_perm("projects.view_project", self.project), True)
        self.assertEqual(self.denied_pentester.has_perm("projects.change_project", self.project), True)
        self.assertEqual(self.denied_pentester.has_perm("projects.delete_project", self.project), True)