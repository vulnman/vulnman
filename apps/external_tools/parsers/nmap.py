from vulnman.utils.tools import ToolResultParser
from libnmap.parser import NmapParser as LibNmapParser


class NmapParser(ToolResultParser):
    """
    Example Command:
    ``nmap -sV -sS -v example.com -oX nmap.xml``
    """
    tool_name = "nmap"

    def parse(self, result, project, creator, command=None):
        nmap_result = LibNmapParser.parse_fromstring(result)
        for nmap_host in nmap_result.hosts:
            host, _created = self._get_or_create_host(nmap_host.address, project, creator, command=command)
            if host.os == "unknown" and nmap_host.os_fingerprinted:
                host.os = nmap_host.os_match_probabilities()[0].name
                host.save()
            for nmap_service in nmap_host.services:
                service, _created = self._get_or_create_service(host, nmap_service.service, nmap_service.port,
                                                                project, creator,
                                                                protocol=nmap_service.protocol, command=command,
                                                                banner=nmap_service.banner, status=nmap_service.state)
                if nmap_service.scripts_results:
                    self._parse_script_results(nmap_service.scripts_results, service, host, project, creator)
            for nmap_hostname in nmap_host.hostnames:
                _hostname, _created = self._get_or_create_hostname(nmap_hostname, host, project, creator,
                                                                   command=command)

    def _parse_script_results(self, results, service, host, project, creator):
        for script_result in results:
            self._get_or_create_finding(script_result.get('id'), script_result.get('output'),
                                        project=project, creator=creator, host=host, service=service)
