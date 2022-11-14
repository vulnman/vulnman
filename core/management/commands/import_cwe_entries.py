import os
import xml.etree.ElementTree as ET
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.findings import models


class Command(BaseCommand):
    help = 'Import vulnerability templates from file'
    cwe_version = "4.9"
    namespace = "http://cwe.mitre.org/cwe-6"

    def handle(self, *args, **options):
        tree = ET.parse(os.path.join(settings.BASE_DIR, "resources/cwec_v%s.xml" % self.cwe_version))
        root = tree.getroot()
        for weakness in root.iter("{%s}Weakness" % self.namespace):
            cwe_id = "CWE-%s" % weakness.attrib["ID"]
            obj, _created = models.CWEEntry.objects.update_or_create(entry=cwe_id, defaults={"name": weakness.attrib.get("Name")})
