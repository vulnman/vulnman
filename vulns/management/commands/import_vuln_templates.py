import csv
from django.core.management.base import BaseCommand
from vulns import models


class Command(BaseCommand):
    help = 'Import vulnerability templates from file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        import_counter = 0
        with open(options['file']) as template_f:
            reader = csv.reader(template_f)
            for row in reader:
                if row[1] == "name":
                    continue
                if row[0] != "":
                    references = "%s\n%s" % (row[0], row[5])
                else:
                    references = row[5]
                references = references.replace("\n ", "\n")
                instance, _created = models.VulnerabilityTemplate.objects.get_or_create(
                    name=row[1], description=row[2], remediation=row[3], exploitation=row[4], references=references)
                if _created:
                    import_counter += 1

        self.stdout.write(self.style.SUCCESS('Successfully imported/updated "%s" templates' % import_counter))
