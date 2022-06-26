from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.management import call_command
from django.utils import timezone
from apps.account.models import User


@shared_task
def send_mail_task(subject, message, to_mail, from_mail=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
    """
    Send a mail using celery
    """
    if not isinstance(to_mail, list):
        to_mail = [to_mail]
    send_mail(subject, message, from_mail, to_mail, fail_silently=fail_silently)


@shared_task
def update_checklists_and_templates():
    call_command("update_checklists")
    call_command("update_vulnerability_templates")


@shared_task
def delete_inactive_users():
    delta = timezone.now() - timezone.timedelta(days=settings.INACTIVE_EXTERNAL_USER_DELETE_DAYS)
    # TODO: do we want this?
    # User.objects.filter(is_active=True, is_vendor=True, last_login__lt=delta).delete()
    User.objects.filter(is_active=False, is_vendor=True, date_joined__lt=delta).delete()

