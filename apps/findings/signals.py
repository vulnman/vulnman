from django.db.models import signals
from django_q.tasks import async_task
from django.conf import settings
from django.dispatch import receiver
from . import models


@receiver(signals.post_save, sender=models.Vulnerability)
def vulnerability_critical_notification(sender, instance=None, created=False, **kwargs):
    if not settings.PROJECTS_NOTIFY_CONTRIBUTORS_ON_CRITICAL:
        return
    if created and instance.severity == models.Vulnerability.SEVERITY_CRITICAL:
        subject = "New Critical Vulnerability created"
        mail_template = "emails/notify_critical_vulnerability.html"
        context = {"vulnerability": instance, "base_url": settings.VULNMAN_BASE_URL}
        contributors = instance.project.projectcontributor_set.values_list("user__email", flat=True)
        to_mails = list(contributors)
        to_mails.append(instance.project.creator.email)
        async_task('vulnman.core.utils.mail.send_mail', subject, mail_template, context,
                   settings.DEFAULT_FROM_EMAIL, to_mails)
