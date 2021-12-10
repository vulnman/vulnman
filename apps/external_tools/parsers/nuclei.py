import json
from urllib.parse import urlparse
from vulnman.utils.tools import ToolResultParser


class Nuclei(ToolResultParser):
    """
    Example Command:
    ``nuclei -json -o nuclei.txt -nc -u http://localhost -t nuclei-templates``
    """
    def parse(self, result, project, creator):
        for line in result.split("\n"):
            try:
                vuln_info = json.loads(line)
                parsed_url = urlparse(vuln_info['host'])
                ip = self._resolve(parsed_url.hostname)
                description = vuln_info['info'].get('description', "Imported from nuclei")
                name = vuln_info['info'].get('name')
                if not name:
                    name = vuln_info['info']['template-id']
                if vuln_info.get('matcher-name'):
                    name = "%s: %s" % (name, vuln_info['matcher-name'])
                references = vuln_info['info'].get('reference')
                if not references:
                    references = []
                if ip:
                    host, _created = self._get_or_create_host(ip, project, creator)
                    if parsed_url.port:
                        service, _created = self._get_or_create_service(host, parsed_url.scheme, parsed_url.port,
                                                                        project, creator)
                    elif parsed_url.scheme and parsed_url.scheme == "https":
                        service, _created = self._get_or_create_service(host, "https", 443, project, creator)
                    else:
                        service, _created = self._get_or_create_service(host, "http", 80, project, creator)
                    # TODO: import curl-command
                    self._get_or_create_vulnerability(
                        name, description, "Imported from nuclei", "Imported from nuclei",
                        '\n'.join(references), project, host=host,
                        cvss_string=vuln_info['info'].get('classification', {}).get('cvss-metrics'),
                        cvss_base_score=vuln_info['info'].get('classification', {}).get('cvss-score'), service=service)
            except json.JSONDecodeError:
                print("Could not decode line: %s" % line)
