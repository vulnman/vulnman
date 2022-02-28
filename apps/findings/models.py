import cvss
import base64
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from vulnman.models import VulnmanModel, VulnmanProjectModel
from apps.findings import constants
from apps.assets.models import ASSET_TYPES_CHOICES, WebApplication


SEVERITY_CHOICES = [
    (4, "critical"),
    (3, "high"),
    (2, "medium"),
    (1, "low"),
    (0, "informational")
]

def get_severity_by_name(name):
    for sev in SEVERITY_CHOICES:
        if sev[1] == name:
            return sev[0]
    return None

class VulnerabilityCategory(VulnmanModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Vulnerability Category"
        verbose_name_plural = "Vulnerability Categories"


class VulnerabilityReference(VulnmanModel):
    url = models.URLField()


class CWEEntry(VulnmanModel):
    entry = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.entry
    

class BaseVulnerability(VulnmanModel):
    severity = models.PositiveIntegerField(choices=SEVERITY_CHOICES)
    name = models.CharField(max_length=256)
    # mitigation = models.TextField()
    description = models.TextField()
    recommendation = models.TextField()
    vulnerability_id = models.CharField(max_length=256)
    cwe_ids = models.ManyToManyField(CWEEntry)
    categories = models.ManyToManyField(VulnerabilityCategory)
    # references = models.ForeignKey(VulnerabiltiyReference)

    class Meta:
        abstract = True


def project_pocs_path(instance, filename):
    return "uploads/proofs/projects/%s/%s" % (instance.pk, filename)


class Vulnerability(VulnmanProjectModel):
    STATUS_OPEN = 0
    STATUS_FIXED = 1
    STATUS_VERIFIED = 2

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_VERIFIED, "Verified"),
        (STATUS_FIXED, "Fixed")
    ]

    template = models.ForeignKey('findings.Template', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    cvss_score = models.FloatField(default=0.0)
    cvss_vector = models.CharField(max_length=64, null=True, blank=True, verbose_name="CVSS Vector")
    cve_id = models.CharField(max_length=28, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_OPEN)
    # generic assets
    asset_type = models.CharField(max_length=64, choices=ASSET_TYPES_CHOICES, default=WebApplication.ASSET_TYPE)
    asset_webapp = models.ForeignKey('assets.WebApplication', on_delete=models.CASCADE, null=True, blank=True)
    asset_webrequest = models.ForeignKey('assets.WebRequest', on_delete=models.CASCADE, null=True, blank=True)
    asset_host = models.ForeignKey('assets.Host', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.template.name

    @property
    def severity(self):
        return self.template.get_severity_display()

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
        return settings.SEVERITY_COLORS[self.severity.capitalize()]

    def get_absolute_url(self):
        return reverse_lazy('projects:findings:vulnerability-detail', kwargs={'pk': self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy('projects:findings:vulnerability-delete', kwargs={'pk': self.pk})

    @property
    def proofs(self):
        proofs = list(self.textproof_set.all()) + list(self.imageproof_set.all())
        proofs.sort(key=lambda proof: proof.order or 0)
        return proofs

    @property
    def asset(self):
        if self.asset_webapp:
            return self.asset_webapp
        elif self.asset_webrequest:
            return self.asset_webrequest
        elif self.asset_host:
            return self.asset_host

    class Meta:
        ordering = ['-cvss_score',]
        verbose_name_plural = "Vulnerabilities"
        verbose_name = "Vulnerability"


class Proof(VulnmanProjectModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(null=True)
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def get_project(self):
        return self.vulnerability.get_project()


class TextProof(Proof):
    text = models.TextField(help_text="Markdown supported!")


class ImageProof(Proof):
    caption = models.CharField(max_length=128, blank=True, null=True)
    image = models.ImageField(max_length=256, upload_to=project_pocs_path)

    def base64_encoded_image(self):
        with open(self.image.path, "rb") as image_f:
            encoded = base64.b64encode(image_f.read())
            return "data:image/png;base64, %s" % encoded.decode()
        #return self.image.path

class Template(BaseVulnerability):
    vulnerability_id = models.CharField(max_length=256, unique=True)

    class Meta:
        ordering = ['vulnerability_id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('findings:template-detail', kwargs={'pk': self.pk})

    def get_risk_level(self):
        return self.vulnerability_set.first().severity


class Reference(VulnmanModel):
    name = models.CharField(max_length=128)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "References"
        verbose_name = "Reference"


class UserAccount(VulnmanProjectModel):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=512)
    role = models.CharField(max_length=128, blank=True, null=True)
    account_compromised = models.BooleanField(default=False)

    def __str__(self):
        return self.username
