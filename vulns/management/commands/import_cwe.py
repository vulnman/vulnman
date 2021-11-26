import re
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from vulns import models


class Command(BaseCommand):
    help = 'Import CWEs from XML'
    namespaces = {
        '': 'http://cwe.mitre.org/cwe-6',
        'xhtml': 'http://www.w3.org/1999/xhtml'
    }

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def find_external_reference(self, root, ref_id):
        reference = root.find('.//External_References/External_Reference[@Reference_ID="%s"]' % ref_id, self.namespaces)
        if reference.find('URL', self.namespaces):
            return reference.find('URL', self.namespaces).text
        elif reference.find('Title', self.namespaces):
            return "'%s' by %s" % (reference.find('Title', self.namespaces).text,
                                   reference.find('Author', self.namespaces).text)
        return reference.text

    def handle(self, *args, **options):
        import_counter = 0
        with open(options['file']) as cwe_f:
            tree = ET.parse(cwe_f)
            root = tree.getroot()
            for weakness in root.findall('.//Weaknesses/Weakness', self.namespaces):
                name = weakness.get('Name')
                cwe_id = weakness.get('ID')
                description = weakness.find('Description', self.namespaces).text
                if weakness.find('Extended_Description', self.namespaces):
                    description = "%s\n%s" % (description,
                                              weakness.find('Extended_Description', self.namespaces).text)
                # TODO: related weaknesses
                impacts = []
                for impact in weakness.findall('.//Common_Consequences/Consequence', self.namespaces):
                    scope = ""
                    for s in impact.findall('Scope', self.namespaces):
                        if s.text == "Other":
                            continue
                        scope = "%s\n%s" % (scope, s.text)
                    impact_str = ""
                    for i in impact.findall('Impact', self.namespaces):
                        if i.text == "Other":
                            continue
                        impact_str = "%s\n%s" % (impact_str, i.text)
                    note = impact.find('Note', self.namespaces)
                    if not note:
                        new_impact = "%s:\n%s\n" % (scope, impact_str)
                    else:
                        new_impact = "%s:\n%s\n%s\n" % (scope, impact_str, note.text)
                    impacts.append(new_impact)
                impact = '\n'.join(impacts)
                mitigations = []
                for mitigation in weakness.findall('.//Potential_Mitigations/Mitigation', self.namespaces):
                    if mitigation.find('Description', self.namespaces).findall('xhtml:p', self.namespaces):
                        desc = ""
                        for p in mitigation.find('Description', self.namespaces).findall('xhtml:p'):
                            desc = "%s\n%s\n" % (desc, p)
                    else:
                        desc = mitigation.find('Description', self.namespaces).text
                    if not mitigation.find('Effectiveness_Notes', self.namespaces):
                        new_mitigation = desc
                    else:
                        new_mitigation = "%s\n%s" % (desc, mitigation.find('Effectiveness_Notes', self.namespaces).text)
                    mitigations.append(new_mitigation)
                mitigation = '\n'.join(mitigations)
                references = ["CWE-%s" % cwe_id]
                if weakness.find('References', self.namespaces):
                    for reference in weakness.findall('.//References/Reference', self.namespaces):
                        if not reference.get('External_Reference_ID'):
                            continue
                        references.append(
                            self.find_external_reference(root, reference.get('External_Reference_ID'))
                        )
                references = '\n'.join(references)
                if models.VulnerabilityTemplate.objects.filter(name=name).exists():
                    self.stdout.write(self.style.WARNING('Template "%s" already exists!' % name))
                    continue
                models.VulnerabilityTemplate.objects.create(name=name, description=description,
                                                            references=references, remediation=mitigation,
                                                            impact=impact)
                import_counter += 1
        self.stdout.write(self.style.SUCCESS('Successfully imported/updated "%s" templates' % import_counter))
