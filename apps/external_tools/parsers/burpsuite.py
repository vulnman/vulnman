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
            service, _created = self.get_or_create_service_from_url(host_url, host, project, creator, command=command)
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
            template, created = self._get_or_create_vulnerability_template(
                name, creator, description=html_to_md(description), ease_of_resolution="undetermined",
                resolution=html_to_md(resolution))
            if created:
                # TODO: create references
                pass
            request = None
            response = None
            for request_response in issue.findall("requestresponse"):
                try:
                    request = base64.b64decode(request_response.find("request").text).decode()
                    response = base64.b64decode(request_response.find("response").text).decode()
                finally:
                    break
            vulnerability, created = self._get_or_create_vulnerability(template, cvss_score,
                                                                       project, creator,
                                                                       details=data, original_name=name,
                                                                       request=request, response=response,
                                                                       path=path, site=site, parameter=parameter,
                                                                       host=host, service=service, command=command)
            # TODO: handle references
