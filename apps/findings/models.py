import cvss
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from vulnman.models import VulnmanModel, VulnmanProjectModel
from apps.findings import constants


def project_pocs_path(instance, filename):
    return "uploads/proofs/projects/%s/%s" % (instance.pk, filename)


class Vulnerability(VulnmanProjectModel):
    name = models.CharField(max_length=128)
    description = models.TextField(help_text="Markdown supported!")
    service = models.ForeignKey('networking.Service', on_delete=models.CASCADE, null=True, blank=True)
    host = models.ForeignKey('networking.Host', on_delete=models.CASCADE, blank=True, null=True)
    cvss_score = models.FloatField(default=0.0)
    cvss_vector = models.CharField(max_length=64, null=True, blank=True, verbose_name="CVSS Vector")
    resolution = models.TextField(blank=True, null=True, help_text="Markdown supported")
    is_fixed = models.BooleanField(default=False)
    ease_of_resolution = models.CharField(choices=constants.FINDINGS_EASE_OF_RESOLUTIONS, max_length=32)

    def __str__(self):
        return self.name

    def get_scores(self):
        if self.cvss_score:
            return [self.cvss_score, self.cvss_score, self.cvss_score]
        if not self.cvss_vector:
            return [0.0, 0.0, 0.0]
        return cvss.CVSS3(self.cvss_vector).scores()

    def get_severities(self):
        if self.cvss_vector:
            return cvss.CVSS3(self.cvss_vector).severities()
        if self.cvss_score >= 9.0:
            return ["Critical", "Critical", "Critical"]
        elif self.cvss_score >= 7.0:
            return ["High", "High", "High"]
        elif self.cvss_score >= 4.0:
            return ["Medium", "Medium", "Medium"]
        elif self.cvss_score >= 0.1:
            return ["Low", "Low", "Low"]
        return ["Information", "Information", "Information"]

    def get_severity_colors(self):
        return settings.SEVERITY_COLORS[self.get_severities()[0]]

    def get_absolute_url(self):
        return reverse_lazy('projects:findings:vulnerability-detail', kwargs={'pk': self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy('projects:findings:vulnerability-delete', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-cvss_score']
        verbose_name_plural = "Vulnerabilities"
        verbose_name = "Vulnerability"


class ProofOfConcept(VulnmanProjectModel):
    name = models.CharField(max_length=64)
    image = models.ImageField(blank=True, upload_to=project_pocs_path, null=True)
    finding = models.ForeignKey(Vulnerability, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Proof of Concepts"
        verbose_name = "Proof of Concept"
        ordering = ["-date_updated"]


"""
# class HTTPFinding(Finding):
#    url = models.URLField()
#    parameter = models.CharField()
#    request = models.TextField()
"""


class Finding(VulnmanProjectModel):
    name = models.CharField(max_length=128)
    data = models.TextField()
    host = models.ForeignKey('networking.Host', on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey('networking.Service', on_delete=models.CASCADE, null=True, blank=True)
    hostname = models.ForeignKey('networking.Hostname', on_delete=models.CASCADE, null=True, blank=True)
    additional_information = models.TextField(blank=True, null=True)
    steps_to_reproduce = models.TextField(blank=True, null=True)
    finding_type = models.CharField(max_length=32, choices=constants.FINDINGS_TYPES, default="undefined")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date_updated"]


class Template(VulnmanModel):
    name = models.CharField(max_length=128)
    description = models.TextField(help_text="Markdown supported!")
    resolution = models.TextField(help_text="Markdown supported")
    ease_of_resolution = models.CharField(choices=constants.FINDINGS_EASE_OF_RESOLUTIONS, max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [('name',)]
        ordering = ["-date_updated"]

    def get_absolute_url(self):
        return reverse_lazy('findings:template-detail', kwargs={'pk': self.pk})


class Reference(VulnmanModel):
    name = models.CharField(max_length=128)
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE, null=True, blank=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class VulnerabilityDetails(VulnmanProjectModel):
    vulnerability = models.OneToOneField(Vulnerability, on_delete=models.CASCADE)
    template = models.OneToOneField(Template, on_delete=models.CASCADE, null=True, blank=True)
    data = models.TextField(help_text="Markdown supported!")
    request = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    method = models.CharField(max_length=12, blank=True, null=True)
    parameter = models.CharField(max_length=128, blank=True, null=True)
    parameters = models.CharField(max_length=256, blank=True, null=True)
    path = models.CharField(max_length=256, blank=True, null=True)
    query_parameters = models.CharField(max_length=256, blank=True, null=True)
    site = models.CharField(max_length=256, blank=True, null=True)
