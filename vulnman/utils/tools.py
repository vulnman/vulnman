import socket
from apps.networking.models import Host, Hostname, Service
from apps.findings.models import Finding, Vulnerability, VulnerabilityDetails


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

    def parse(self, result, project, creator):
        """
        This method is called when a tool report is imported

        :param result: content of the tool report as string
        :param project: the :class:`~apps.projects.models.Project` instance this report belongs to
        :param creator: the :class:`django.contrib.auth.models.User` instance this report was created
        :return: None
        """
        raise NotImplementedError

    def _get_or_create_host(self, ip, project, creator):
        """
        get or create a :class:`~vulns.models.Host`
        :param ip: the ip of the host
        :param project: the project this host belongs to
        :param creator: the user which creates the host
        :return: instance of :class:`~vulns.models.Host`
        """
        return Host.objects.get_or_create(ip=ip, project=project, defaults={'creator': creator})

    def _get_or_create_hostname(self, name, host, project, creator):
        """
        get or create a :class:`~vulns.models.Hostname`
        :param name: hostname
        :param host: the host this hostname belongs to
        :return: instance of :class:`~vulns.models.Hostname`
        """
        return Hostname.objects.get_or_create(host=host, name=name, project=project, defaults={"creator": creator})

    def _get_or_create_service(self, host, name, port, project, creator, protocol="tcp", status="open", banner=None):
        """

        :param host: the host this service is running on
        :param name: name of the service (e.g. "http")
        :param port: the port number
        :param protocol: protocol of the service (default: "tcp")
        :param status: status of the service (default: "open")
        :return: instance of :class:`~vulns.models.Host`
        """
        return Service.objects.get_or_create(host=host, name=name, port=port, protocol=protocol, project=project,
                                             defaults={"creator": creator, "status": status, "banner": banner})

    def _get_or_create_finding(self, name, data, project, creator, additional_information=None, reproduce=None,
                               host=None, service=None, hostname=None):
        return Finding.objects.get_or_create(project=project, name=name, data=data,
                                             additional_information=additional_information,
                                             steps_to_reproduce=reproduce, hostname=hostname, service=service,
                                             host=host, defaults={"creator": creator})

    def _get_or_create_vulnerability(self, name, description, cvss_score, resolution, project,
                                     creator, ease_of_resolution="undetermined", host=None, service=None,
                                     details_data=None):
        if details_data:
            filter_data = {}
            for key, value in details_data.items():
                filter_data["vulnerabilitydetails__%s" % key] = value
            filter_data.update({"name": name, "description": description,
                                "project": project, "host": host, "service": service})
            if Vulnerability.objects.filter(**filter_data).exists():
                vulnerability = Vulnerability.objects.get(**filter_data)
                return vulnerability, False
            else:
                vulnerability = Vulnerability.objects.create(creator=creator, ease_of_resolution=ease_of_resolution,
                                                             cvss_score=cvss_score, resolution=resolution,
                                                             project=project, name=name, description=description,
                                                             host=host, service=service)
                details = VulnerabilityDetails.objects.create(vulnerability=vulnerability, project=project,
                                                              creator=creator, **details_data)
                return vulnerability, True

        return Vulnerability.objects.get_or_create(project=project, host=host, service=service, name=name,
                                                   description=description, resolution=resolution,
                                                   defaults={"creator": creator, "cvss_score": cvss_score,
                                                             "ease_of_resolution": ease_of_resolution})

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
