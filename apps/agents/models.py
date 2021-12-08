import binascii
import os
from django.db import models
from django.contrib.auth.models import User
from vulnman.models import VulnmanModel
from rest_framework.authtoken.models import Token


class AgentQueue(VulnmanModel):
    parsed_command = models.TextField()
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)

    def __str__(self):
        return self.parsed_command[:256]


class Agent(Token):
    key = models.CharField(max_length=128, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=28)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(32)).decode()
