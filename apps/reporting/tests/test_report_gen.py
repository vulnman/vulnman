from django.test import TestCase
from django_q.tasks import async_task, result
from vulnman.tests.mixins import VulnmanTestMixin
from apps.reporting import models
from apps.reporting import tasks


class ReportGeneratorTestCase(TestCase, VulnmanTestMixin):
    def setUp(self):
        self.init_mixin()

    def test_create_report_task(self):
        report = self._create_instance(models.Report, project=self.project1)
        release = self._create_instance(models.ReportRelease, report=report, project=self.project1)
        task_id = async_task(tasks.do_create_report, release.pk, sync=True)
        task_result = result(task_id, 200)
        self.assertEqual(task_result[0], True)
        self.assertEqual(models.ReportRelease.objects.filter(compiled_source__isnull=False).count(), 1)
