from django.utils import timezone
from django.conf import settings
from vulnman.core.utils.mail import send_mail
from .models import Vulnerability


def notify_disclosure_date():
    subject = settings.RESPONSIBLE_DISCLOSURE_NOTIFY_MAIL_SUBJECT
    for vuln in Vulnerability.objects.filter(is_published=False):
        notify_date = vuln.date_planned_disclosure - timezone.timedelta(
            days=settings.RESPONSIBLE_DISCLOSURE_NOTIFY_DAYS_BEFORE_DISCLOSURE)
        today = timezone.now().date()
        if (today >= notify_date) and (today <= vuln.date_planned_disclosure):
            context = {"vulnerability": vuln}
            # Notify creator
            send_mail(subject, "responsible_disc/emails/notification_planned_disclosure.html",
                      context, settings.RESPONSIBLE_DISCLOSURE_MAIL_FROM, vuln.user.email)
    return True
