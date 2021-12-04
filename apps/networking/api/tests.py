from vulnman.tests.mixins import VulnmanTestMixin
from rest_framework.test import APITestCase
from apps.networking import models
from apps.networking.api import serializers


class HostTestCases(APITestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_unauth_list(self):
        url = self.get_url("api:networking:host-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_list_view(self):
        url = self.get_url("api:networking:host-list")
        my_host = self._create_instance(models.Host, project__creator=self.user1)
        not_my_host = self._create_instance(models.Host, project__creator=self.user2)
        self.assertEqual(models.Host.objects.filter(project__creator=self.user1).count(), 1)
        self.assertEqual(models.Host.objects.filter(project__creator=self.user2).count(), 1)
        self.client.force_login(self.user1)
        # test if i can see only my hosts
        response = self.client.get(url)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["uuid"], serializers.HostSerializer(my_host).data["uuid"])
