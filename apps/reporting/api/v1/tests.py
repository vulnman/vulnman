from rest_framework.test import APITestCase
from vulnman.api.tests.testcase import VulnmanAPITestCaseMixin
from apps.reporting import models


class PentestReportViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()
        self.forbidden_project = self.create_project()
        self.account1 = self.create_instance(models.UserAccount, project=self.project)
        self.account2 = self.create_instance(models.UserAccount, project=self.forbidden_project)

    def test_report_create(self):
        # TODO: implement
        pass
