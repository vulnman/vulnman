import cvss
import base64
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from vulnman.models import VulnmanModel, VulnmanProjectModel
from apps.findings import constants
from apps.tagging.models import UUIDTaggedItem


def project_pocs_path(instance, filename):
    return "uploads/proofs/projects/%s/%s" % (instance.pk, filename)


class Vulnerability(VulnmanProjectModel):
    template = models.ForeignKey('findings.Template', on_delete=models.CASCADE)
    service = models.ForeignKey('networking.Service', on_delete=models.CASCADE, null=True, blank=True)
    host = models.ForeignKey('networking.Host', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=128)
    details = models.TextField(help_text="Markdown supported!", null=True, blank=True)
    cvss_score = models.FloatField(default=0.0)
    cvss_vector = models.CharField(max_length=64, null=True, blank=True, verbose_name="CVSS Vector")
    # usually web vulnerability require the following fields
    request = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    method = models.CharField(max_length=12, blank=True, null=True)
    parameter = models.CharField(max_length=128, blank=True, null=True)
    parameters = models.CharField(max_length=256, blank=True, null=True)
    path = models.CharField(max_length=256, blank=True, null=True)
    query_parameters = models.CharField(max_length=256, blank=True, null=True)
    site = models.CharField(max_length=256, blank=True, null=True)
    # general
    is_fixed = models.BooleanField(default=False)
    false_positive = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    original_name = models.CharField(max_length=128, null=True, blank=True)
    tags = TaggableManager(through=UUIDTaggedItem, blank=True)

    def __str__(self):
        return self.template.name

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

    @property
    def proofs(self):
        proofs = list(self.textproof_set.all()) + list(self.imageproof_set.all())
        proofs.sort(key=lambda proof: proof.order or 0)
        return proofs

    class Meta:
        ordering = ['-cvss_score', '-verified']
        verbose_name_plural = "Vulnerabilities"
        verbose_name = "Vulnerability"


class Proof(VulnmanProjectModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(null=True)
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TextProof(Proof):
    text = models.TextField(help_text="Markdown supported!")


class ImageProof(Proof):
    caption = models.TextField(blank=True, null=True)
    image = models.ImageField(max_length=256, upload_to=project_pocs_path)

    def base64_encoded_image(self):
        if self.image:
            with open(self.image.path, "rb") as image_f:
                encoded = base64.b64encode(image_f.read())
                return "data:image/png;base64, %s" % encoded.decode()


class ProofOfConcept(VulnmanProjectModel):
    # TODO: deprecate
    name = models.CharField(max_length=64)
    image = models.ImageField(blank=True, upload_to=project_pocs_path, null=True)
    finding = models.ForeignKey(Vulnerability, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    is_code = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Proof of Concepts"
        verbose_name = "Proof of Concept"
        ordering = ["-date_updated"]

    def base64_encoded_image(self):
        if self.image:
            with open(self.image.path, "rb") as image_f:
                encoded = base64.b64encode(image_f.read())
                return "data:image/png;base64, %s" % encoded.decode()


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
    cve_id = models.CharField(max_length=64, null=True, blank=True, verbose_name="CVE ID")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [('name',)]
        ordering = ["-date_updated"]

    def get_absolute_url(self):
        return reverse_lazy('findings:template-detail', kwargs={'pk': self.pk})


class Reference(VulnmanModel):
    name = models.CharField(max_length=128)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "References"
        verbose_name = "Reference"


"""
class Technology(VulnmanModel):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    maintained = models.BooleanField(blank=True, null=True)
    homepage = models.URLField(blank=True, null=True)
    icon = models.CharField(max_length=28, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Technologies"
        verbose_name = "Technology"
        ordering = ["-date_updated"]
        unique_together = [('name',)]


class Product(VulnmanProjectModel):
    # a product that we pentest
    name = models.CharField(max_length=128)
"""
