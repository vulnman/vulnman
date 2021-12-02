from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from uuid import uuid4


class Methodology(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('methodology:methodology-detail', kwargs={'pk': self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy('methodology:methodology-delete', kwargs={'pk': self.pk})


class SuggestedCommand(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=32)
    tool_name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True, null=True)
    command = models.TextField()
    methodology = models.ForeignKey(Methodology, on_delete=models.CASCADE)

    def __str__(self):
        return self.tool_name

    def parse_command(self, target_ip=None, target_domain=None, target_port=None, target_scheme=None):
        command = self.command
        if target_ip:
            command = command.replace("%target_ip%", target_ip)
        if target_domain:
            command = command.replace("%target_domain%", target_domain)
        if target_port:
            command = command.replace("%target_port%", target_port)
        if target_scheme:
            command = command.replace("%target_scheme%", target_scheme)
        return command

    class Meta:
        verbose_name_plural = "Suggested Commands"
        verbose_name = "Suggested Command"
        unique_together = [("methodology", "name")]
