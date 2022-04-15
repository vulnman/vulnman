from rest_framework.authentication import TokenAuthentication
from apps.projects.models import ProjectAPIToken


class AgentTokenAuthentication(TokenAuthentication):
    model = ProjectAPIToken
