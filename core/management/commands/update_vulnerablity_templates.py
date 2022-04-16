from django.core.management.base import BaseCommand
from django.core.management import call_command
from core.utils.template_updater import update_vulnerability_templates


class Command(BaseCommand):
    help = 'Update Vulnerability Template Repository'

    def handle(self, *args, **options):
        update_vulnerability_templates()
        call_command("import_vulnerability_templates")
