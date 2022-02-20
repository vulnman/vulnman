from rest_framework.test import APITestCase
from vulnman.tests.mixins import VulnmanAPITestMixin
from apps.commands import models


class CommandTemplateTestCase(object):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        obj = self._create_instance(models.CommandTemplate)
        url = self.get_url("api:v1:command-template-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(obj.pk))

    def test_createview(self):
        url = self.get_url("api:v1:command-template-list")
        payload = {"command": "gobuster dir -u %target_scheme%://%target_domain%:%target_port% -w wordlist.txt -e",
                   "name": "gobuster-dir", "tool_name": "gobuster"}
        self.client.force_login(self.user1)
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.CommandTemplate.objects.filter(creator=self.user1).count(), 1)

    def test_detailview(self):
        pass

    def test_deleteview(self):
        obj = self._create_instance(models.CommandTemplate)
        url = self.get_url("api:v1:command-template-detail", pk=obj.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


class CommandHistoryAPITestCase(APITestCase, VulnmanAPITestMixin):
    def setUp(self):
        self.init_mixin()

    def test_history_push(self):
        payload = {"command": "ping -c 1 1.1.1", "output": "test", "exit_code": 0}
        self._test_project_createview("api:v1:command-history-push", payload, models.CommandHistoryItem)
