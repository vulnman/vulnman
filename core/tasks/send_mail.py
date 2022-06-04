from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_mail_task(subject, message, to_mail, from_mail=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
    """
    Send a mail using celery
    """
    if not isinstance(to_mail, list):
        to_mail = [to_mail]
    send_mail(subject, message, from_mail, to_mail, fail_silently=fail_silently)
