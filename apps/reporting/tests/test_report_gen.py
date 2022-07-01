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
        report = self._create_instance(models.Report, project=self.project1)
        release = self._create_instance(models.ReportRelease, report=report, project=self.project1)
        task = tasks.do_create_report.delay(release.pk)
        result = task.get()
        self.assertEqual(result[0], True)
        self.assertEqual(models.ReportRelease.objects.filter(compiled_source__isnull=False).count(), 1)
