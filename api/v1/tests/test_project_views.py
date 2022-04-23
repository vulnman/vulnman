from rest_framework.test import APITestCase
from api.v1.mixins import VulnmanAPITestCaseMixin


class ProjectViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("api:v1:project-list")
        self.login_with_project(self.pentester1, self.project1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(self.project1.pk))
