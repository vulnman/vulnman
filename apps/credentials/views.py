from vulnman.views import generic
from credentials import models


class CredentialList(generic.ProjectListView):
	context_object_name = "credentials"
	template_name = "credentials/credentials_list.html"
	model = models.Credentials
