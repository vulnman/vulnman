import binascii
import os
from django.urls import reverse_lazy
from django.db import models
from django.contrib.auth.models import User
from vulnman.models import VulnmanProjectModel
from rest_framework.authtoken.models import Token
from apps.projects.models import Project


class AgentQueue(VulnmanProjectModel):
    command = models.TextField()
    exit_code = models.IntegerField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    agent = models.ForeignKey('agents.Agent', on_delete=models.SET_NULL, null=True, blank=True)
    in_progress = models.BooleanField(default=False)
    execution_started = models.DateTimeField(null=True, blank=True)
    execution_ended = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.command[:256]

    class Meta:
        ordering = ["-date_updated"]

    @staticmethod
    def has_push_permission(request):
        project = request.data.get('project')
        if project and Project.objects.filter(pk=project, creator=request.user).exists():
            return True
        return False


class Agent(Token):
    key2 = models.CharField(max_length=128, primary_key=True)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE)
    name2 = models.CharField(max_length=28)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(32)).decode()

    def get_absolute_delete_url(self):
        return reverse_lazy('agents:agent-delete', kwargs={'pk': self.pk})
