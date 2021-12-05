from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.conf import settings


class Host(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    ip = models.GenericIPAddressField(verbose_name="IP")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    os = models.CharField(max_length=28, default="unknown", verbose_name="OS")
    is_online = models.BooleanField(default=True)

    def __str__(self):
        return str(self.ip)

    def get_absolute_url(self):
        return reverse_lazy('projects:networking:host-detail', kwargs={'pk': self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy('projects:networking:host-delete', kwargs={'pk': self.pk})

    def get_hostnames(self):
        if not self.hostname_set.exists():
            return "-"
        return ', '.join(self.hostname_set.values_list('name', flat=True))

    def get_host_icon(self):
        for key, value in settings.HOST_OS_ICONS.items():
            for match in value.get('matches', []):
                if match in self.os:
                    return value.get('icon')
        return ""

    class Meta:
        unique_together = [('ip', 'project')]
        ordering = ["-date_updated"]


class Hostname(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Hostnames"
        unique_together = [('host', 'name')]

    @property
    def project(self):
        return self.host.project


class Service(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    port = models.IntegerField()
    protocol = models.CharField(max_length=12, default="tcp")
    banner = models.CharField(max_length=256, blank=True, null=True)
    status = models.CharField(max_length=24, default="open")

    def __str__(self):
        return "%s/%s" % (self.port, self.protocol)

    @property
    def project(self):
        return self.host.project
