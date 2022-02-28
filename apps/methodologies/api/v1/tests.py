from rest_framework.test import APITestCase
from vulnman.api.tests.testcase import VulnmanAPITestCaseMixin
from apps.methodologies import models
from apps.assets.models import WebApplication


class TaskViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_task_list(self):
        self.create_instance(models.Task)
        url = self.get_url("api:v1:task-list")
        self.client.force_login(self.project_pentester)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)


class AssetTaskViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_asset_task_list(self):
        asset = self.create_instance(WebApplication, project=self.project)
        task = self.create_instance(models.Task)
        asset_task = self.create_instance(models.AssetTask, task=task, project=self.project, asset_webapp=asset)
        self.client.force_login(self.project_pentester)
        url = self.get_url("api:v1:asset-task-detail", pk=str(asset_task.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project"], str(self.project.pk))

    def test_asset_task_create(self):
        pass

    def test_asset_task_delete(self):
        pass
