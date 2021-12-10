import os
from django.conf import settings
from django.core.management.base import BaseCommand
from vulnman.utils.secret import generate_secret_key


class Command(BaseCommand):
    help = 'Create Secret Key'

    def handle(self, *args, **options):
        if not os.path.exists(os.path.join(settings.BASE_DIR, 'vulnman/secret_key.py')):
            generate_secret_key(os.path.join(settings.BASE_DIR, 'vulnman/secret_key.py'))
