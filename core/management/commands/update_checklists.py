import os
from django.conf import settings
from django.core.management.base import BaseCommand
from git import Repo
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Update Checklist Repository'

    def handle(self, *args, **options):
        template_dir = os.path.join(
            settings.BASE_DIR, "resources/checklists")
        if os.path.isdir(template_dir):
            repo = Repo(template_dir)
            origin = repo.remotes.origin
            origin.pull()
        else:
            Repo.clone_from(settings.CHECKLIST_REPO, template_dir)

        call_command("import_checklists")
