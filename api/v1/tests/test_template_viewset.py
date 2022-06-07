from rest_framework.test import APITestCase
from api.v1.mixins.testcase import VulnmanAPITestCaseMixin
from apps.findings import models


class TemplateViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_forbidden_create_method(self):
        url = self.get_url("api:v1:vulnerability-template-list")
        payload = {"data": "lorem"}
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 405)

    def test_forbidden_delete_method(self):
        obj = self.create_instance(models.Template)
        url = self.get_url("api:v1:vulnerability-template-detail", pk=str(obj.pk))
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)

    def test_listview(self):
        self.create_instance(models.Template)
        url = self.get_url("api:v1:vulnerability-template-list")
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 1)
