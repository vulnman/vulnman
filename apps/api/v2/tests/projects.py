from rest_framework.test import APITestCase
from vulnman.api.tests import VulnmanAPITestCaseMixin


class ProjectViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("")
