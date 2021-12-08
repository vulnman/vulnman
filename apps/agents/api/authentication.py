from rest_framework.authentication import TokenAuthentication
from apps.agents import models


class AgentAuthentication(TokenAuthentication):
    model = models.Agent
