from rest_framework.test import APITestCase
from api.v1.mixins import VulnmanAPITestCaseMixin
from apps.assets import models


class TemplateViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_forbidden_create_method(self):
        url = self.get_url("api:v1:host-list")
        payload = {"data": "lorem"}
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 405)

    def test_forbidden_delete_method(self):
        obj = self.create_instance(models.Host)
        url = self.get_url("api:v1:host-detail", pk=str(obj.pk))
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)

    def test_listview(self):
        self.create_instance(models.Host, project=self.project1)
        url = self.get_url("api:v1:host-list")
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 1)

    def test_auth_required(self):
        url = self.get_url("api:v1:host-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_project_object_filter(self):
        self.create_instance(models.Host, project=self.project2)
        url = self.get_url("api:v1:host-list")
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 0)

    def test_permission_required(self):
        host = self.create_instance(models.Host, project=self.project1)
        url = self.get_url("api:v1:host-detail", pk=str(host.pk))
        self.login_with_project(self.pentester2, self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

