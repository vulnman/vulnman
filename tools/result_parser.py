from vulns.models import Host, Hostname, Service


class ToolResultParser(object):
	def parse(self, result, project, creator):
		"""
		This method is called when a tool report is imported

		:param result: content of the tool report as string
		:param project: project instance of the corresponding project
		:param creator: the user that has uploaded the report
		:return: None
		"""
		raise NotImplementedError

	def _get_or_create_host(self, ip, project, creator):
		return Host.objects.get_or_create(ip=ip, project=project, defaults={'creator': creator})

	def _get_or_create_hostname(self, name, host):
		return Hostname.objects.get_or_create(host=host, name=name)

	def _get_or_create_service(self, host, name, port, protocol="tcp", status="up"):
		return Service.objects.get_or_create(host=host, name=name, port=port, protocol=protocol, status=status)
