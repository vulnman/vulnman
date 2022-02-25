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
        url = self.get_url("api:v1:report-update", pk=str(report.pk))
        data = {"mgmt_summary_evaluation": "This is a *test*", "mgmt_summary_recommendation": "This is another **test**"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 401)
        self.client.force_login(self.denied_pentester)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.project_pentester)
        response = self.client.patch(url, data)
        self.assertEqual(models.PentestReport.objects.filter(mgmt_summary_evaluation=data["mgmt_summary_evaluation"]).count(), 1)
