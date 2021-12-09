from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from uuid import uuid4
from vulnman.models import VulnmanModel

"""
class Finding(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128)
    template = models.ForeignKey('vulns.VulnerabilityTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(help_text="Markdown supported")
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    service = models.ForeignKey('networking.Service', on_delete=models.CASCADE, null=True, blank=True)
    host = models.ForeignKey('networking.Host', on_delete=models.CASCADE, null=True, blank=True)
    cvss_score = models.FloatField(default=0.0)

    cvss_vector = models.CharField(max_length=64, null=True, blank=True, verbose_name="CVSS Vector")
    is_fixed = models.BooleanField(default=False)
    references = models.TextField(blank=True, null=True)
    remediation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-cvss_score']

# class HTTPFinding(Finding):
#    url = models.URLField()
#    parameter = models.CharField()
#    request = models.TextField()


def project_pocs_path(instance, filename):
    return "uploads/proofs/projects/%s/%s" % (instance.pk, filename)


class ProofOfConcept(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    image = models.ImageField(blank=True, upload_to=project_pocs_path, null=True)
    finding = models.ForeignKey(Finding, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Proof of Concepts"
        verbose_name = "Proof of Concept"
"""


class Template(VulnmanModel):
    name = models.CharField(max_length=128)
    description = models.TextField(help_text="Markdown supported!")
    remediation = models.TextField(help_text="Markdown supported")
    references = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [('name',)]
        ordering = ["-date_updated"]

    def get_absolute_url(self):
        return reverse_lazy('findings:template-detail', kwargs={'pk': self.pk})
