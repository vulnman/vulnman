import cvss
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from uuid import uuid4


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
        return reverse_lazy('projects:vulns:host-detail', kwargs={'pk': self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy('projects:vulns:host-delete', kwargs={'pk': self.pk})

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


class Vulnerability(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vulnerability_template = models.ForeignKey('vulns.VulnerabilityTemplate', on_delete=models.SET_NULL,
                                               null=True, blank=True)
    name = models.CharField(max_length=128)
    description = models.TextField(help_text="Markdown supported")
    cvss_string = models.CharField(max_length=64, null=True, blank=True, verbose_name="CVSS Vector")
    cvss_base_score = models.FloatField(null=True, blank=True)
    impact = models.TextField()
    remediation = models.TextField()
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, null=True, blank=True)
    is_fixed = models.BooleanField(default=False)
    references = models.TextField()

    def __str__(self):
        return self.name

    def get_scores(self):
        if not self.cvss_string:
            return [0.0, 0.0, 0.0]
        return cvss.CVSS3(self.cvss_string).scores()

    def get_severities(self):
        if not self.cvss_string:
            return ["None", "None", "None"]
        return cvss.CVSS3(self.cvss_string).severities()

    def get_severity_colors(self):
        return settings.SEVERITY_COLORS[self.get_severities()[0]]

    def get_absolute_url(self):
        return reverse_lazy('projects:vulns:vuln-detail', kwargs={'pk': self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy('projects:vulns:vuln-delete', kwargs={'pk': self.pk})

    def get_references_as_list(self):
        return self.references.split("\n")

    class Meta:
        ordering = ['-cvss_base_score']


def project_pocs_path(instance, filename):
    return "uploads/proofs/projects/%s/%s" % (instance.pk, filename)


class ProofOfConcept(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    image = models.ImageField(blank=True, upload_to=project_pocs_path, null=True)
    vuln = models.ForeignKey(Vulnerability, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Proof of Concepts"
        verbose_name = "Proof of Concept"


class VulnerabilityTemplate(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    remediation = models.TextField()
    impact = models.TextField()
    references = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('vulns:vuln-template-detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = [('name',)]


class WebApplicationUrlPath(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    path = models.CharField(max_length=512, unique=True)
    full_url = models.URLField(max_length=512, unique=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    hostname = models.ForeignKey(Hostname, on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    status_code = models.IntegerField(default=200)
    web_application = models.ForeignKey('webapps.WebApplication', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.path
