from rest_framework.test import APITestCase
from vulnman.core.test import VulnmanAPITestCaseMixin
from apps.methodologies import models


class TaskViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_forbidden_create_method(self):
        url = self.get_url("api:ui:methodologies:task-list")
        payload = {"data": "lorem"}
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 405)

    def test_forbidden_delete_method(self):
        obj = self._create_instance(models.Task)
        url = self.get_url("api:ui:methodologies:task-detail", pk=str(obj.pk))
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)

    def test_listview(self):
        self._create_instance(models.Task)
        url = self.get_url("api:ui:methodologies:task-list")
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 1)

    def test_auth_required(self):
        url = self.get_url("api:ui:methodologies:task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
