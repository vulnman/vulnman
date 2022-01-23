from django.test import TestCase
from django.utils import timezone
from vulnman.tests.mixins import VulnmanTestMixin
from apps.projects.models import Client
from apps.reporting import models


class ReportViewsTestCase(TestCase, VulnmanTestMixin):
    def setUp(self) -> None:
        self.init_mixin()

    def test_createview(self):
        url = self.get_url("projects:reporting:report-create")
        client = self._create_instance(Client, name="iamarandomclientfromthetestcase")
        project = self._create_project(creator=self.user1, client=client)
        self.assign_perm("projects.pentest_project", self.pentester, obj=project)
        payload = {"revision": "0.1.0", "changes": "test123"}
        self.login_with_project(self.pentester, project)
        #response = self.client.post(url, payload)
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(models.Report.objects.count(), 1)
        # TODO: make tests work with celery again
        # self.assertEqual(project.client.name in models.Report.objects.first().raw_source, True)
        # self.assertEqual(models.Report.objects.filter(raw_source__isnull=False).count(), 1)

    def test_report_share_token_validation(self):
        report = self._create_instance(models.Report)
        token = models.ReportShareToken.objects.create(report=report,
                                                       date_expires=timezone.now() - timezone.timedelta(days=1))
        self.assertIsNotNone(token.share_token)
        # check expired token is expired
        self.assertEqual(models.ReportShareToken.is_expired(token.share_token), True)
        # check token is valid
        token.date_expires = timezone.now() + timezone.timedelta(days=1)
        token.save()
        self.assertEqual(models.ReportShareToken.is_expired(token.share_token), False)

    def test_shared_report_access(self):
        report = self._create_instance(models.Report)
        token = models.ReportShareToken.objects.create(report=report,
                                                       date_expires=timezone.now() + timezone.timedelta(days=1))
        url = self.get_url("projects:reporting:report-shared-report-detail", pk=report.pk, token=token.share_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        token.date_expires = timezone.now() - timezone.timedelta(days=1)
        token.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
