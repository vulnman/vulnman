import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django_q.models import Schedule


class Command(BaseCommand):
    help = 'Initialize notification tasks'

    def handle(self, *args, **options):
        # Notification mail when a vulnerability is about to be disclosed soon
        Schedule.objects.create(func='apps.responsible_disc.notifications.notify_disclosure_date', schedule_type=Schedule.CRON, repeats="-1", cron="0 0 * * *")
