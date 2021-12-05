import re
from vulnman.utils.tools import ToolResultParser
from apps.social.models import Employee


class Infoga(ToolResultParser):
    def parse(self, result, project, creator):
        for item in re.findall(r"(Email: )(.*\s)(\()(\d.*)(\))", result):
            employee, _created = Employee.objects.get_or_create(email=item[1], project=project, creator=creator)
