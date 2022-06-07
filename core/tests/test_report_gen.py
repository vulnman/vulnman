from django.test import TestCase
from django.conf import settings
from vulnman.tests.mixins import VulnmanTestMixin
from apps.reporting import models
from apps.reporting import tasks


class ReportGeneratorTestCase(TestCase, VulnmanTestMixin):
    def setUp(self):
        self.init_mixin()
        settings.TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
        settings.CELERY_TASK_ALWAYS_EAGER = True

    def test_create_report_task(self):
        task = tasks.do_create_report.delay(self.project1.reportinformation.pk, "draft")
        _result = task.get()
        self.assertEqual(models.PentestReport.objects.count(), 1)
