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
