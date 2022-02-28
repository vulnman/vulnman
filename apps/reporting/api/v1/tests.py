from rest_framework.test import APITestCase
from vulnman.api.tests.testcase import VulnmanAPITestCaseMixin
from apps.reporting import models


class PentestReportViewSetTestCase(APITestCase, VulnmanAPITestCaseMixin):
    def setUp(self):
        self.init_mixin()

    def test_report_create(self):
        # TODO: implement
        pass

    def test_report_update(self):
        report = self.create_instance(models.PentestReport, project=self.project)
        url = self.get_url("api:v1:report-information-list")
        data = {"evaluation": "This is a *test*", "recommendation": "This is another **test**", "project": str(self.project.pk), "author": self.project_pentester.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        self.client.force_login(self.denied_pentester)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.client.force_login(self.project_pentester)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.ReportInformation.objects.filter(evaluation=data["evaluation"]).count(), 1)
