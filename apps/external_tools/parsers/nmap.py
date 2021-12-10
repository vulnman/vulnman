from vulnman.utils.tools import ToolResultParser
from libnmap.parser import NmapParser as LibNmapParser


class NmapParser(ToolResultParser):
    """
    Example Command:
    ``nmap -sV -sS -v example.com -oX nmap.xml``
    """
    def parse(self, result, project, creator):
        nmap_result = LibNmapParser.parse_fromstring(result)
        for nmap_host in nmap_result.hosts:
            host, _created = self._get_or_create_host(nmap_host.address, project, creator)
            if host.os == "unknown" and nmap_host.os_fingerprinted:
                # TODO: implement
                pass
            for nmap_service in nmap_host.services:
                _service, _created = self._get_or_create_service(host, nmap_service.service, nmap_service.port,
                                                                 project, creator,
                                                                 protocol=nmap_service.protocol,
                                                                 banner=nmap_service.banner, status=nmap_service.state)
            for nmap_hostname in nmap_host.hostnames:
                _hostname, _created = self._get_or_create_hostname(nmap_hostname, host, project, creator)
