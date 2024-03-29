from django.utils import timezone
from rest_framework.authentication import TokenAuthentication as BasicTokenAuthentication
from rest_framework import exceptions
from apps.projects.models import ProjectAPIToken


class TokenAuthentication(BasicTokenAuthentication):
    model = ProjectAPIToken

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if timezone.now().date() > token.date_valid:
            token.delete()
            raise exceptions.AuthenticationFailed("Token expired")
        return user, token
