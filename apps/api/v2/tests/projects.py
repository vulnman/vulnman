from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ddf import G
from vulnman.api.tests import VulnmanAPITestCaseMixin


class ProjectViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_listview(self):
        url = self.get_url("")
