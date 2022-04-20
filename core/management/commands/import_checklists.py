import yaml
import os
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import Task, TaskCondition


class Command(BaseCommand):
    help = 'Import checklists'

    def handle(self, *args, **options):
        import_counter = 0
        for path in Path(os.path.join(settings.BASE_DIR, 'resources/checklists')).rglob('info.yaml'):
            if "_template" in str(path):
                continue
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
            task, created = Task.objects.update_or_create(
                task_id=item["id"], defaults={
                    "name": item["name"],
                    "description": description})
            TaskCondition.objects.filter(task=task).delete()
            for condition in item.get("conditions", []):
                asset_type = list(condition.keys())[0].split(".")[0]
                attr = list(condition.keys())[0].split(".")[1]
                TaskCondition.objects.update_or_create(
                    task=task, asset_type=asset_type, name=attr,
                    condition=list(condition.values())[0]
                )

