import socket
from vulnman.utils.tools import ToolResultParser
from urllib.parse import urlparse


class GenericURL(ToolResultParser):
    tool_name = "generic-url"

    def parse(self, result, project, creator, command=None):
        for line in result.split("\n"):
            parsed = urlparse(line)
            try:
                host_ip = socket.gethostbyname(parsed.netloc)
            except socket.error:
                print("Could not resolve %s" % parsed.netloc)
                continue
            host, _created = self._get_or_create_host(host_ip, project, creator, command=command)
            if not parsed.port:
                if parsed.scheme == "https":
                    service, _created = self._get_or_create_service(host, parsed.scheme, 443, project, creator,
                                                                    command=command)
                else:
                    service, _created = self._get_or_create_service(host, parsed.scheme, 80, project, creator,
                                                                    command=command)
            else:
                service, _created = self._get_or_create_service(host, parsed.scheme, parsed.port, project, creator,
                                                                command=command)
            if parsed.netloc:
                hostname, _created = self._get_or_create_hostname(parsed.netloc, host, project, creator,
                                                                  command=command)
            else:
                hostname = None
            reproduce = "curl %s" % parsed.geturl()
            self._get_or_create_finding("Found Web Path", parsed.path, project, creator,
                                        additional_information=line.replace("\n", ""), reproduce=reproduce,
                                        host=host, service=service, hostname=hostname, command=command)


class GenericDomains(ToolResultParser):
    tool_name = "generic-domains"

    def parse(self, result, project, creator, command=None):
        for line in result.split("\n"):
            try:
                host_ip = socket.gethostbyname(line)
            except socket.error:
                print("Could not resolve %s" % line)
                continue
            host, _created = self._get_or_create_host(host_ip, project, creator, command=command)
            self._get_or_create_hostname(line, host, project, creator, command=command)
