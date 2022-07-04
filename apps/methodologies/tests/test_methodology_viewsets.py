from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase
from vulnman.tests.mixins import VulnmanAPITestMixin, VulnmanTestMixin
from apps.methodologies import models


class MethodologyViewSet(APITestCase, VulnmanAPITestMixin):
    def setUp(self):
        self.init_mixin()

    def test_task_search(self):
        obj = self._create_instance(models.Task, name="testtasklorem")
        url = self.get_url("api:v1:task-list")
        url += "?search=testtasklorem"
        self.client.force_login(self.pentester1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("results", [])[0]["uuid"], str(obj.pk))


class ChecklistViewsTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_checklist_list(self):
        url = self.get_url("methodology:methodology-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_URL) + "?next=" + url)
        self.client.force_login(self.pentester1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
