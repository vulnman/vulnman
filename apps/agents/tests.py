from django.test import TestCase
from vulnman.tests.mixins import VulnmanTestMixin
from apps.agents import models


class AgentTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("agents:agent-list")
        _agent = self._create_instance(models.Agent, user=self.user1)
        self._test_unauthenticated_aceess(url, expected_status_code=200)
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['agents']), 1)
        # test other user
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['agents']), 0)
