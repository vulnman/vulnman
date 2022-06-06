from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from apps.projects.models import ProjectAPIToken


class AgentTokenAuthentication(TokenAuthentication):
    model = ProjectAPIToken

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if timezone.now().date() > token.date_valid:
            raise exceptions.AuthenticationFailed("Token expired")
        return user, token
