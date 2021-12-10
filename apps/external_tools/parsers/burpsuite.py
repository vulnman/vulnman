import xml.etree.ElementTree as ET
import base64
import re
from urllib.parse import urlparse
from vulnman.utils.tools import ToolResultParser


SEVERITY_MAP = {
    "Critical": "9.0",
    "High": "7.0",
    "Medium": "4.0",
    "Low": "1.0",
    "Information": "0.0"
}


class BurpSuiteProXML(ToolResultParser):
    def parse(self, result, project, creator):
        root = ET.fromstring(result)
        for issue in root.findall("issue"):
            host_ip = issue.find("host").get("ip")
            host, _created = self._get_or_create_host(host_ip, project, creator)
            host_url = issue.find("host").text
            parsed_url = urlparse(host_url)
            if parsed_url.port:
                service, _created = self._get_or_create_service(
                    host, parsed_url.scheme, parsed_url.port, project, creator)
            elif parsed_url.scheme == "https":
                service, _created = self._get_or_create_service(host, "https", 443, project, creator)
            else:
                service, _created = self._get_or_create_service(host, "http", 80, project, creator)
            hostname, _created = self._get_or_create_hostname(parsed_url.hostname, host, project, creator)
            name = issue.find("name").text
            description = ""
            resolution = ""
            issue_detail_dict = {
                "path": issue.find("path").text, "site": issue.find("host").text
            }
            if "parameter" in issue.find("location").text:
                issue_detail_dict["parameter"] = re.search(r"(\[)(.*)(\s)", issue.find('location').text).group(2)
            issue_detail_str = "The vulnerability was found at %s" % issue.find("location").text
            if issue.find("issueBackground") is not None:
                description += issue.find("issueBackground").text.replace("<p>", "").replace(
                    "<br>", "\n").replace("</p>", "\n")
            if issue.find("remediationBackground") is not None:
                resolution += issue.find("remediationBackground").text.replace("<p>", "").replace(
                    "<br>", "\n").replace("</p>", "\n")
            if issue.find("remediationDetail") is not None:
                resolution += issue.find("remediationDetail").text.replace("<p>", "").replace(
                    "<br>", "\n").replace("</p>", "\n")
            if issue.find("issueDetail") is not None:
                issue_detail_dict["data"] = issue.find("issueDetail").text.replace("<p>", "").replace(
                    "<br>", "\n").replace("</p>", "\n")
            cvss_score = SEVERITY_MAP.get(issue.find("severity").text)
            vulnerability, created = self._get_or_create_vulnerability(name, description, cvss_score,
                                                                       resolution, project, creator,
                                                                       host=host, service=service,
                                                                       details_data=issue_detail_dict)
            # TODO: handle references
            # TODO: handle request and response details
