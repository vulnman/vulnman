import json
from urllib.parse import urlparse
from vulnman.utils.tools import ToolResultParser


class Nuclei(ToolResultParser):
    """
    Example Command:
    ``nuclei -json -o nuclei.txt -nc -u http://localhost -t nuclei-templates``
    """
    tool_name = "nuclei"

    def parse(self, result, project, creator, command=None):
        # TODO: handle curl-command
        # TODO: handle references
        # TODO: handle matched-at
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
                    vuln_value = vuln_info["matcher-name"]
                    name = "%s: %s" % (name, vuln_info["matcher-name"])
                else:
                    vuln_value = vuln_info["matched-at"]
                references = vuln_info['info'].get('reference')
                if not references:
                    references = []
                if ip:
                    host, _created = self._get_or_create_host(ip, project, creator)
                    hostname, _created = self._get_or_create_hostname(parsed_url.hostname, host, project,
                                                                      creator, command=command)
                    service, _created = self.get_or_create_service_from_url(vuln_info['host'], host, project, creator)
                    cvss_score = vuln_info['info'].get('classification', {}).get('cvss-score', 0.0)
                    vulnerability, created = self._get_or_create_vulnerability(
                        name, description, cvss_score, project, creator, detail_data=vuln_value, command=command,
                        service=service, host=host)
                    if created:
                        self._create_vulnerability_details(vulnerability, vuln_value, site=parsed_url.geturl())
            except json.JSONDecodeError:
                print("Could not decode line: %s" % line)
