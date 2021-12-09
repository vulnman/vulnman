from django.db import models
from vulnman.models import VulnmanModel, VulnmanProjectModel

COMMAND_PLACEHOLDERS = [
    "%target_ip%", "%target_domain%", "%target_port%", "%target_scheme%"
]


class CommandTemplate(VulnmanModel):
    name = models.CharField(max_length=64)
    tool_name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True, null=True)
    command = models.TextField(
        help_text="The following placeholders are available: %s" % ','.join(COMMAND_PLACEHOLDERS))

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
        verbose_name_plural = "Command Templates"
        verbose_name = "Command Template"
        unique_together = [("name", "tool_name")]
        ordering = ["-date_updated"]


class CommandHistoryItem(VulnmanProjectModel):
    command = models.TextField()
    exit_code = models.IntegerField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    agent = models.ForeignKey('agents.Agent', on_delete=models.SET_NULL, null=True, blank=True)
