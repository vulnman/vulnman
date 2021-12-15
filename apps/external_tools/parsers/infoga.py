import re
from vulnman.utils.tools import ToolResultParser
from apps.social.models import Employee


class Infoga(ToolResultParser):
    """
    Example Command:
    ``ìnfoga --domain example.com -r tesla.txt``
    """
    tool_name = "infoga"

    def parse(self, result, project, creator, command=None):
        for item in re.findall(r"(Email: )(.*\s)(\()(\d.*)(\))", result):
            employee, _created = Employee.objects.get_or_create(email=item[1], project=project, creator=creator,
                                                                command_created=command)
