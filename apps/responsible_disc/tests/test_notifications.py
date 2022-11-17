from django.test import TestCase, override_settings
from django.utils import timezone
from django.conf import settings
from django.core import mail
from vulnman.core.test import VulnmanTestCaseMixin
from apps.responsible_disc import models
from apps.responsible_disc import notifications


class NotificationTestCase(TestCase, VulnmanTestCaseMixin):
    def setUp(self):
        self.init_mixin()
        settings.Q_CLUSTER["sync"] = True
        disclosure_date1 = timezone.now().date() + timezone.timedelta(days=3)
        disclosure_date2 = timezone.now().date() - timezone.timedelta(days=3)
        self.vuln1 = self.create_instance(models.Vulnerability, is_published=False,
                                          user=self.pentester1, date_planned_disclosure=disclosure_date1)
        self.vuln2 = self.create_instance(models.Vulnerability, is_published=False,
                                          user=self.pentester2, date_planned_disclosure=disclosure_date2)

    def test_notification_correct_amount(self):
        notifications.notify_disclosure_date()
        self.assertEqual(len(mail.outbox), 1)
        self.vuln2.date_planned_disclosure = timezone.now().date() + timezone.timedelta(days=3)
        self.vuln2.save()
        notifications.notify_disclosure_date()
        self.assertEqual(len(mail.outbox), 3)

    def test_correct_receipient(self):
        notifications.notify_disclosure_date()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.pentester1.email])
