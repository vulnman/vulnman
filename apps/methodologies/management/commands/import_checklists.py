import yaml
import os
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.methodologies import models


class Command(BaseCommand):
    help = 'Import checklists'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def handle(self, *args, **options):
        import_counter = 0
        if options.get('file'):
            self._import_file(options.get('file'), import_counter)
        else:
            for path in Path(os.path.join(settings.BASE_DIR, 'resources/checklists')).rglob('info.yaml'):
                self._import_file(path, import_counter)
        self.stdout.write(self.style.SUCCESS('Successfully imported/updated "%s" templates' % import_counter))

    def _get_description(self, filename):
        desc_filename = str(filename).replace("info.yaml", "ReadMe.md")
        with open(desc_filename) as f:
            return f.read()

    def _import_file(self, filename, import_counter):
        with open(filename, "r") as f:
            item = yaml.safe_load(f)
            description = self._get_description(filename)
            template, created = models.Task.objects.update_or_create(task_id=item["id"], defaults={"name": item["name"], "description": description})
            if created:
                import_counter += 1
