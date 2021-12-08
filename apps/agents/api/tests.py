from rest_framework.test import APITestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.agents import models


class AgentAPITestCase(APITestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()
        self.agent1 = models.Agent.objects.create(key="unique1", user=self.user1, name="test-agent-1")
        self.agent2 = models.Agent.objects.create(key="unique2", user=self.user2, name="test-agent-2")

    def test_queue_list(self):
        # test unauthenticated
        url = self.get_url("api:agents:queue-list")
        # test unauthenticated
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        # test session auth is disabled
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        queue_item = self._create_instance(models.AgentQueue, project__creator=self.user1)
        response = self.client.get(url, HTTP_AUTHORIZATION="Token %s" % self.agent1.key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)
        # test other user
        response = self.client.get(url, HTTP_AUTHORIZATION="Token %s" % self.agent2.key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 0)
