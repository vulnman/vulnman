from rest_framework.test import APITestCase
from apps.api.v2.mixins import VulnmanAPITestCaseMixin


class MethodologyViewSet(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_task_search(self):
        url = self.get_url("api:v1:task-list")
        url += "?search=sql"
        self.client.force_login(self.pentester1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
