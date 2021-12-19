import xml.etree.ElementTree as ET
import base64
import re
from urllib.parse import urlparse
from vulnman.utils.tools import ToolResultParser
from vulnman.utils.markdown import html_to_md


SEVERITY_MAP = {
    "Critical": "9.0",
    "High": "7.0",
    "Medium": "4.0",
    "Low": "1.0",
    "Information": "0.0"
}


class BurpSuiteProXML(ToolResultParser):
    """
    Plugin to parse BurpSuite Pro XML reports
    """
    def parse(self, result, project, creator, command=None):
        root = ET.fromstring(result)
        for issue in root.findall("issue"):
            host_ip = issue.find("host").get("ip")
            host, _created = self._get_or_create_host(host_ip, project, creator, command=command)
            host_url = issue.find("host").text
            parsed_url = urlparse(host_url)
            if parsed_url.port:
                service, _created = self._get_or_create_service(
                    host, parsed_url.scheme, parsed_url.port, project, creator, command=command)
            elif parsed_url.scheme == "https":
                service, _created = self._get_or_create_service(host, "https", 443, project, creator, command=command)
            else:
                service, _created = self._get_or_create_service(host, "http", 80, project, creator, command=command)
            hostname, _created = self._get_or_create_hostname(parsed_url.hostname, host, project, creator,
                                                              command=command)
            name = issue.find("name").text
            description = ""
            resolution = ""
            parameter = None
            path = issue.find("path").text
            site = issue.find("host").text
            data = None
            if "parameter" in issue.find("location").text:
                parameter = re.search(r"(\[)(.*)(\s)", issue.find('location').text).group(2)
            if issue.find("issueBackground") is not None:
                description += html_to_md(issue.find("issueBackground").text.replace("<p>", "").replace(
                    "<br>", "\n").replace("</p>", "\n"))
            if issue.find("remediationBackground") is not None:
                resolution += html_to_md(issue.find("remediationBackground").text.replace("<p>", "").replace(
                    "<br>", "\n").replace("</p>", "\n"))
            if issue.find("remediationDetail") is not None:
                resolution += html_to_md(issue.find("remediationDetail").text.replace("<p>", "").replace(
                    "<br>", "\n").replace("</p>", "\n"))
            if issue.find("issueDetail") is not None:
                data = html_to_md(issue.find("issueDetail").text.replace("<p>", "").replace(
                    "<br>", "\n").replace("</p>", "\n"))
            else:
                data = description
            cvss_score = SEVERITY_MAP.get(issue.find("severity").text)
            vulnerability, created = self._get_or_create_vulnerability(name, html_to_md(description), cvss_score,
                                                                       project, creator,
                                                                       resolution=html_to_md(resolution),
                                                                       detail_data=data,
                                                                       path=path, site=site, parameter=parameter,
                                                                       host=host, service=service, command=command)
            if created:
                self._create_vulnerability_details(vulnerability, data, path=path, site=site, parameter=parameter)
            # TODO: handle references
            # TODO: handle request and response details
