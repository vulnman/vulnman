import json
from vulnman.utils.tools import ToolResultParser
from apps.findings.models import Reference


class TestSSL(ToolResultParser):
    """
    Example Command:
    ``testssl --json example.com:443``
    """
    def parse(self, result, project, creator):
        j = json.loads(result)
        service_name = "unknown"
        for item in j:
            if item["id"] == "service":
                service_name = item["finding"].lower()
                break
        for item in j:
            if item["severity"] == "OK" or item["id"] == "scanTime":
                continue
            elif item["severity"] == "INFO":
                # TODO: maybe handle later
                continue
            if len(item["ip"].split("/")) == 2 and item["ip"].split("/")[-1]:
                host_ip = item["ip"].split("/")[1]
                host, _created = self._get_or_create_host(host_ip, project, creator)
                hostname, _created = self._get_or_create_hostname(item["ip"].split("/")[0], host, project, creator)
                service, _created = self._get_or_create_service(host, service_name, item["port"], project, creator)
                vulnerability, _created = self._get_or_create_vulnerability(
                    item["id"], item["finding"],
                    self._get_score_by_severity(item["severity"]), "Disable cipher",
                    project, creator, host=host, service=service)
                for ref in item.get("cve", "").split(" "):
                    if ref:
                        Reference.objects.create(vulnerability=vulnerability, creator=creator, name=ref)
                for ref in item.get("cwe", "").split(" "):
                    if ref:
                        Reference.objects.create(vulnerability=vulnerability, creator=creator, name=ref)
