import socket
import re
from urllib.parse import urlparse
from vulnman.utils.tools import ToolResultParser
from vulns.models import WebApplicationUrlPath


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
                self._get_or_create_hostname(subdomain, host)


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
                    hostname, _created = self._get_or_create_hostname(parsed.hostname, host)
                    if not parsed.port:
                        if parsed.scheme == "https":
                            service, _created = self._get_or_create_service(host, "https", 443)
                        else:
                            service, _created = self._get_or_create_service(host, "http", 80)
                    else:
                        service, _created = self._get_or_create_service(host, parsed.scheme, parsed.port)
                    status_code = re.search(r"(Status: )([\d]+)", line).group(2)
                    webapp_url, _created = WebApplicationUrlPath.objects.get_or_create(
                        service=service, hostname=hostname, project=project, status_code=status_code,
                        full_url=url_path[0], path=parsed.path, defaults={'creator': creator})
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
                _hostname, _created = self._get_or_create_hostname(item[1], host)
