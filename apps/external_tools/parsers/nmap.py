from vulnman.utils.tools import ToolResultParser
from libnmap.parser import NmapParser as LibNmapParser
from vulns import models


class NmapParser(ToolResultParser):
    def parse(self, result, project, creator):
        nmap_result = LibNmapParser.parse_fromstring(result)
        for nmap_host in nmap_result.hosts:
            host, _created = models.Host.objects.get_or_create(ip=nmap_host.address, project=project,
                                                               defaults={'creator': creator})
            if host.os == "unknown" and nmap_host.os_fingerprinted:
                # TODO: implement
                pass
            for nmap_service in nmap_host.services:
                service, _created = models.Service.objects.get_or_create(
                    host=host, port=nmap_service.port, protocol=nmap_service.protocol,
                    defaults={
                        "name": nmap_service.service, "banner": nmap_service.banner, "status": nmap_service.state
                    })
            for nmap_hostname in nmap_host.hostnames:
                hostname, _created = models.Hostname.objects.get_or_create(host=host, name=nmap_hostname)
