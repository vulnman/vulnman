from vulnman.utils.tools import ToolResultParser
import re


class Fierce(ToolResultParser):
    """
    Example Command:
    ``fierce -domain tesla.com | tee fierce.txt``
    """
    def parse(self, result, project, creator):
        for item in re.findall(r"(Found: )(.*\s)(\()(\d.*)(\))", result):
            host, _created = self._get_or_create_host(item[3], project, creator)
            _hostname, _created = self._get_or_create_hostname(item[1][:-2], host, project, creator)
