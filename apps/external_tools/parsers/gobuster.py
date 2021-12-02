import socket
from urllib.parse import urlparse
from vulnman.utils.tools import ToolResultParser
from vulns.models import Host, Hostname, Service, WebApplicationUrlPath


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
                host, _created = Host.objects.get_or_create(ip=host_ip, project=project, defaults={'creator': creator})
                self._get_or_create_hostname(subdomain, host)


# dir plugin
class GobusterDir(ToolResultParser):
    def parse(self, result, project, creator):
        for line in result.split("\n"):
            if "Status:" not in line and "Size:" not in line:
                continue
            url_path = line.split(" ")
            try:
                parsed = urlparse(url_path[0])
                try:
                    host_ip = socket.gethostbyname(parsed.hostname)
                    host, _created = Host.objects.get_or_create(
                        ip=host_ip, project=project, defaults={'creator': creator})
                    hostname, _created = Hostname.objects.get_or_create(host=host, name=parsed.hostname)
                    if not parsed.port:
                        if parsed.scheme == "https":
                            service, _created = Service.objects.get_or_create(host=host, name="https", port=443)
                        else:
                            service, _created = Service.objects.get_or_create(host=host, name="http", port=80)
                    else:
                        service, _created = Service.objects.get_or_create(
                            host=host, name=parsed.scheme, port=parsed.port)
                    status_code = url_path[-3].replace(")", "")
                    webapp_url, _created = WebApplicationUrlPath.objects.get_or_create(
                        service=service, hostname=hostname, project=project, status_code=status_code,
                        full_url=url_path[0], path=parsed.path, defaults={'creator': creator})
                except socket.error:
                    print("Could not resolve subdomain %s" % parsed.hostname)
                    continue
            except Exception as e:
                print(e)
