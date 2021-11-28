import socket
from tools.result_parser import ToolResultParser
from vulns.models import Host, Hostname


class GobusterVhost(ToolResultParser):
    def parse(self, result, project, creator):
        for line in result.split("\n"):
            if "Found: " in line:
                subdomain = line.split(" ")[1]
                try:
                    host_ip = socket.gethostbyname(subdomain)
                except socket.error:
                    print("Could not resolve subdomain %s" % subdomain)
                    continue
                host, _created = Host.objects.get_or_create(ip=host_ip, project=project, defaults={'creator': creator})
                Hostname.objects.get_or_create(host=host, name=subdomain)
