from vulnman.utils.tools import ToolResultParser


class Subfinder(ToolResultParser):
    """
    Example command:
    ``subfinder -d example.com | tee subfinder.txt``
    """
    def parse(self, result, project, creator):
        for line in result.split("\n"):
            resolved_ip = self._resolve(line)
            if resolved_ip:
                host, _created = self._get_or_create_host(resolved_ip, project, creator)
                _hostname, _created = self._get_or_create_hostname(line.replace("\n", ""), host, project, creator)
