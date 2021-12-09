from rest_framework.test import APITestCase
from vulnman.tests.mixins import VulnmanAPITestMixin
from apps.agents import models


class AgentAPITestCase(APITestCase, VulnmanAPITestMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.agent1 = models.Agent.objects.create(key="unique1", user=self.user1, name="test-agent-1")
        self.agent2 = models.Agent.objects.create(key="unique2", user=self.user2, name="test-agent-2")

    def test_queue_list(self):
        # test unauthenticated
        url = self.get_url("api:v1:agent-queue-list")
        # test unauthenticated
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        # test session auth is disabled
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        # test valid user
        queue_item = self._create_instance(models.AgentQueue, project__creator=self.user1)
        response = self.client.get(url, HTTP_AUTHORIZATION="Token %s" % self.agent1.key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)
        # test other user
        response = self.client.get(url, HTTP_AUTHORIZATION="Token %s" % self.agent2.key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 0)

    def test_queue_push(self):
        project = self._create_project(name="queuepush", creator=self.user1)
        payload = {"command": 'echo "1"', "project": str(project.pk)}
        url = self.get_url("api:v1:agent-queue-push")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user2)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user1)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.AgentQueue.objects.filter(project=project).count(), 1)
        self.assertEqual(models.AgentQueue.objects.filter(command='echo "1"').count(), 1)

    def test_queue_update(self):
        obj = self._create_instance(models.AgentQueue, project__creator=self.user1, command="before")
        payload = {"command": "after", "in_progress": True}
        url = self.get_url("api:v1:agent-queue-detail", pk=obj.pk)
        response = self.client.patch(url, payload, HTTP_AUTHORIZATION="Token %s" % self.agent1.key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.AgentQueue.objects.filter(command="before").count(), 1)
        self.assertEqual(models.AgentQueue.objects.filter(agent=self.agent1).count(), 1)
        # test task ended
        payload = {"exit_code": "0", "output": "results"}
        response = self.client.patch(url, payload, HTTP_AUTHORIZATION="Token %s" % self.agent1.key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.AgentQueue.objects.filter(in_progress=False, exit_code=0, output="results").count(), 1)
