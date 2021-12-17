import re
import socket
from urllib.parse import urlparse
from django.db.models import Q
from difflib import SequenceMatcher
from apps.networking.models import Host, Hostname, Service
from apps.findings.models import Finding, Vulnerability, VulnerabilityDetails, Template
from apps.findings.constants import VULNERABILITY_SEVERITY_MAP


class ToolResultParser(object):
    """
    This is the parent class for all external tool importers.
    """
    tool_name = None

    def get_tool_name(self):
        if not self.tool_name:
            return "Invalid Name!"
            # raise ImproperlyConfigured("Plugin does not have a tool name set!")
        return self.tool_name

    def parse(self, result, project, creator, command=None):
        """
        This method is called when a tool report is imported

        :param result: content of the tool report as string
        :param project: the :class:`~apps.projects.models.Project` instance this report belongs to
        :param creator: the :class:`django.contrib.auth.models.User` instance this report was created
        :param command: the :class:`~apps.commands.models.CommandHistoryItem` instance this report belongs to
        :return: None
        """
        raise NotImplementedError

    def _get_or_create_host(self, ip, project, creator, command=None):
        """
        get or create a :class:`~vulns.models.Host`
        :param ip: the ip of the host
        :param project: the project this host belongs to
        :param creator: the user which creates the host
        :return: instance of :class:`~vulns.models.Host`
        """
        return Host.objects.get_or_create(ip=ip, project=project,
                                          defaults={'creator': creator, 'command_created': command})

    def _get_or_create_hostname(self, name, host, project, creator, command=None):
        """
        get or create a :class:`~vulns.models.Hostname`
        :param name: hostname
        :param host: the host this hostname belongs to
        :return: instance of :class:`~vulns.models.Hostname`
        """
        return Hostname.objects.get_or_create(host=host, name=name, project=project,
                                              defaults={"creator": creator, 'command_created': command})

    def _get_or_create_service(self, host, name, port, project, creator, protocol="tcp", status="open", banner=None,
                               command=None):
        """

        :param host: the host this service is running on
        :param name: name of the service (e.g. "http")
        :param port: the port number
        :param protocol: protocol of the service (default: "tcp")
        :param status: status of the service (default: "open")
        :return: instance of :class:`~vulns.models.Host`
        """
        return Service.objects.get_or_create(host=host, port=port, protocol=protocol, project=project,
                                             defaults={"creator": creator, "status": status, "banner": banner,
                                                       "name": name, 'command_created': command})

    def _get_or_create_finding(self, name, data, project, creator, additional_information=None, reproduce=None,
                               host=None, service=None, hostname=None, command=None, finding_type=None):
        return Finding.objects.get_or_create(project=project, name=name, data=data,
                                             additional_information=additional_information,
                                             hostname=hostname, service=service, finding_type=finding_type,
                                             host=host, defaults={"creator": creator, 'command_created': command,
                                                                  'steps_to_reproduce': reproduce})

    def _vulnerability_exists(self, name, vulnerability_data, project, host=None, service=None, method=None,
                              parameter=None, path=None, site=None):
        vulnerability_details = VulnerabilityDetails.objects.filter(data=vulnerability_data, method=method,
                                                                    parameter=parameter, path=path, site=site,
                                                                    project=project, vulnerability__host=host,
                                                                    vulnerability__service=service,
                                                                    vulnerability__name=name)
        if not vulnerability_details.exists():
            return None
            #try:
            #    return Vulnerability.objects.get(name=name, host=host, service=service, project=project)
            #except Vulnerability.DoesNotExist:
            #    return None
        try:
            return Vulnerability.objects.get(name=name, host=host, service=service, project=project,
                                             vulnerabilitydetails=vulnerability_details.get())
        except Vulnerability.DoesNotExist:
            return None

    def _get_or_create_vulnerability(self, name, description, cvss_score, project, creator, resolution=None,
                                     ease_of_resolution="undetermined", host=None, service=None, command=None,
                                     cvss_vector=None,
                                     path=None, site=None, detail_data=None, method=None, parameter=None):
        possible_vuln = self._vulnerability_exists(name, detail_data, project, host=host, service=service,
                                                   method=method, path=path, parameter=parameter, site=site)
        if possible_vuln:
            return possible_vuln, False
        vulnerability_template = self._get_vulnerability_template_or_none(name, detail_data)
        if vulnerability_template:
            if hasattr(vulnerability_template, 'vulnerabilitydetails'):
                possible_vuln = self._vulnerability_exists(
                    vulnerability_template.name, detail_data, project, host=host, service=service,
                    method=vulnerability_template.vulnerabilitydetails.method)
                if possible_vuln:
                    return possible_vuln, False
            else:
                possible_vuln = self._vulnerability_exists(
                    vulnerability_template.name, detail_data, project, host=host, service=service)
                if possible_vuln:
                    return possible_vuln, False
            vulnerability = Vulnerability.objects.create(
                project=project, host=host, service=service, name=vulnerability_template.name,
                description=vulnerability_template.description, resolution=vulnerability_template.resolution,
                ease_of_resolution=vulnerability_template.ease_of_resolution,
                command_created=command, creator=creator, cvss_score=cvss_score, cvss_vector=cvss_vector)
            return vulnerability, True
        return Vulnerability.objects.create(
            project=project, host=host, service=service, name=name, description=description, resolution=resolution,
            ease_of_resolution=ease_of_resolution, command_created=command, creator=creator,
            cvss_score=cvss_score, cvss_vector=cvss_vector), True

    def _create_vulnerability_details(self, vulnerability, data, method=None, path=None, parameter=None,
                                      parameters=None, request=None, response=None, query_params=None, site=None):
        return VulnerabilityDetails.objects.create(vulnerability=vulnerability, data=data, method=method, path=path,
                                                   project=vulnerability.project, creator=vulnerability.creator,
                                                   parameter=parameter, parameters=parameters, request=request,
                                                   response=response, query_parameters=query_params, site=site)

    def _resolve(self, hostname: str):
        """
        resolve a hostname and return ip as string

        :param hostname: hostname
        :return: str: ip
        """
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None

    def _get_score_by_severity(self, severity):
        severity = severity.lower()
        return VULNERABILITY_SEVERITY_MAP.get(severity)

    def _get_vulnerability_template_or_none(self, name, details=None, similarity=0.7):
        # replace special chars with spaces to tokenize them
        # name = re.sub(r"[^a-zA-Z0-9\n\.]", r" ", name.lower())
        name = name.lower()
        name_tokens = name.lower().split(" ")
        conditions = None
        for token in name_tokens:
            if conditions is None:
                conditions = Q(name__contains=token)
            else:
                conditions |= Q(name__contains=token)
        if conditions is None:
            return None
        templates = Template.objects.filter(conditions)
        ratios = []
        for template in templates:
            # handle special cases for imported CWEs
            if "('%s')" % name in template.name.lower():
                template_name = template.name.lower().rsplit("(", 1)[-1].replace(")", "").replace("'", "")
            else:
                template_name = template.name.lower()
            sim_ratio = SequenceMatcher(None, name, template_name).ratio()
            if sim_ratio >= similarity:
                ratios.append((sim_ratio, template))
        if ratios:
            # sort ratios list of tuples by ratios
            ratios.sort(key=lambda x: x[0])
            return ratios[0][1]
        return None

    def get_or_create_service_from_url(self, url, host, project, creator):
        parsed = urlparse(url)
        if parsed.port:
            service, created = self._get_or_create_service(host, parsed.scheme, parsed.port,
                                                            project, creator)
        elif parsed.scheme and parsed.scheme == "https":
            service, created = self._get_or_create_service(host, "https", 443, project, creator)
        else:
            service, created = self._get_or_create_service(host, "http", 80, project, creator)
        return service, created
