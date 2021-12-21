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
                cve_id = None
                if not name:
                    name = vuln_info['info']['template-id']
                if "cve-" in vuln_info.get('template-id', "").lower():
                    cve_id = vuln_info.get('template-id')
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
                    if self.is_finding(name):
                        finding_type = self.get_finding_type(name)
                        finding, _created = self._get_or_create_finding(name, vuln_value, project, creator,
                                                                        reproduce=vuln_info.get('curl-command'),
                                                                        command=command, service=service, host=host,
                                                                        hostname=hostname, finding_type=finding_type)
                    else:
                        template, _created = self._get_or_create_vulnerability_template(
                            name, creator, ease_of_resolution="undetermined", description=description,
                            resolution="", cve_id=cve_id)
                        vulnerability, created = self._get_or_create_vulnerability(
                            template, cvss_score, project, creator, command, service=service, host=host,
                            path=parsed_url.path, original_name=name,
                            site=parsed_url.geturl(), details=vuln_value)
                        if created and vuln_info.get('curl-command'):
                            command_str = "```%s```" % vuln_info.get('curl-command')
                            self._create_proof_of_concept(vulnerability, "Reproduce", project, creator,
                                                          description=command_str, command=command, is_code=True)
            except json.JSONDecodeError:
                print("Could not decode line: %s" % line)

    def is_finding(self, name):
        matchers = ["Wappalyzer", "WAF Detection"]
        for matcher in matchers:
            if matcher in name:
                return True
        return False

    def get_finding_type(self, name):
        tech_matchers = ["Technology", "version detect"]
        for tech_matcher in tech_matchers:
            if tech_matcher in name.lower():
                return "tech"
        return "undefined"
