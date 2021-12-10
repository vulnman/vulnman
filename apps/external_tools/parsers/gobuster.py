import socket
import re
from urllib.parse import urlparse
from vulnman.utils.tools import ToolResultParser


# vhost plugin
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
                host, _created = self._get_or_create_host(host_ip, project, creator)
                self._get_or_create_hostname(subdomain, host, project, creator)


# dir plugin
class GobusterDir(ToolResultParser):
    tool_name = "gobuster dir"

    def parse(self, result, project, creator):
        for line in result.split("\n"):
            if "Status:" not in line and "Size:" not in line:
                continue
            url_path = line.split(" ")
            try:
                parsed = urlparse(url_path[0])
                try:
                    host_ip = socket.gethostbyname(parsed.hostname)
                    host, _created = self._get_or_create_host(host_ip, project, creator)
                    hostname, _created = self._get_or_create_hostname(parsed.hostname, host, project, creator)
                    if not parsed.port:
                        if parsed.scheme == "https":
                            service, _created = self._get_or_create_service(host, "https", 443, project, creator)
                        else:
                            service, _created = self._get_or_create_service(host, "http", 80, project, creator)
                    else:
                        service, _created = self._get_or_create_service(host, parsed.scheme, parsed.port,
                                                                        project, creator)
                    reproduce = "curl %s" % url_path[0]
                    self._get_or_create_finding("Found Web Path", parsed.path, project, creator,
                                                additional_information=line.replace("\n", ""), reproduce=reproduce,
                                                host=host, service=service, hostname=hostname)
                except socket.error:
                    print("Could not resolve subdomain %s" % parsed.hostname)
                    continue
            except Exception as e:
                print(e)


# dns
class GobusterDNS(ToolResultParser):
    """
    Example Command:
    ``gobuster dns -w subdomains.txt -d example.com | tee gobuster-dns.txt``
    """
    def parse(self, result, project, creator):
        for item in re.findall(r"(Found: )(.*)", result):
            ip = self._resolve(item[1])
            if ip:
                host, _created = self._get_or_create_host(ip, project, creator)
                _hostname, _created = self._get_or_create_hostname(item[1], host, project, creator)
