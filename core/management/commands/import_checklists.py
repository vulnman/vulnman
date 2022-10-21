import sys
import warnings
import yaml
import os
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from apps.checklists import models


class Command(BaseCommand):
    help = 'Import checklists from application'
    counter_created_t = 0
    counter_updated_t = 0

    def add_arguments(self, parser):
        parser.add_argument('app_name')

    def get_app_path(self, app_name):
        return os.path.join(apps.get_app_config(app_name).path, "checklists")

    def handle(self, *args, **options):
        app_name = options["app_name"]
        for path in Path(self.get_app_path(app_name)).rglob('info.yaml'):
            if "_template/info.yaml" in str(path):
                continue
            self._import_file(path)
        self.stdout.write(self.style.SUCCESS(
            "Successfully imported ckecklists! Created: {created}, Updated: {updated}".format(
                created=self.counter_created_t, updated=self.counter_updated_t)
        ))

    def _get_readme(self, filename):
        desc_filename = str(filename).replace("info.yaml", "ReadMe.md")
        if not os.path.exists(desc_filename):
            return sys.stdout.write("ReadMe.md missing for !")
        with open(desc_filename, "r") as f:
            return f.read()

    def _import_file(self, filename):
        with open(filename, "r") as f:
            for item in yaml.safe_load(f):
                checklist, created = models.ChecklistTask.objects.get_or_create(
                    task_id=item["id"], defaults={"name": item["name"], "description": self._get_readme(filename)})
                if created:
                    self.counter_created_t += 1
                else:
                    self.counter_updated_t += 1
                # remove old conditions
                models.Condition.objects.filter(task=checklist).delete()
                for condition in item.get("conditions", []):
                    asset_type, name = list(condition.keys())[0].split(".")
                    value = list(condition.values())[0]
                    cond, _created = models.Condition.objects.get_or_create(task=checklist, on_asset_type=asset_type,
                                                                            name=name, value=value)
