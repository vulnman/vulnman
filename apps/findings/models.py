import cvss
import os
import base64
from django.db import models
from django.urls import reverse_lazy
from django.dispatch import receiver
from vulnman.models import VulnmanModel, VulnmanProjectModel
from apps.assets.models import ASSET_TYPES_CHOICES, WebApplication


SEVERITY_CHOICES = [
    (4, "Critical"),
    (3, "High"),
    (2, "Medium"),
    (1, "Low"),
    (0, "Informational")
]


def get_severity_by_name(name):
    for sev in SEVERITY_CHOICES:
        if sev[1] == name:
            return sev[0]
    return None


class VulnerabilityCategory(VulnmanModel):
    name = models.CharField(max_length=128, unique=True)
    display_name = models.CharField(max_length=128, null=True)

    def __str__(self):
        if self.display_name:
            return self.display_name
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
    description = models.TextField()
    recommendation = models.TextField()
    vulnerability_id = models.CharField(max_length=256)
    cwe_ids = models.ManyToManyField(CWEEntry)
    categories = models.ManyToManyField(VulnerabilityCategory)
    # references = models.ForeignKey(VulnerabiltiyReference)

    class Meta:
        abstract = True


class BaseCVSS(models.Model):
    # Attack Vector
    CVSS_AV_NETWORK = "N"
    CVSS_AV_ADJACENT = "A"
    CVSS_AV_LOCAL = "L"
    CVSS_AV_PHYSICAL = "P"
    CVSS_AV_CHOICES = [
        (CVSS_AV_NETWORK, "Network (N)"), (CVSS_AV_PHYSICAL, "Physical (P)"),
        (CVSS_AV_ADJACENT, "Adjacent (A)", )
    ]

    # Attack Complexity
    CVSS_AC_LOW = "L"
    CVSS_AC_HIGH = "H"
    CVSS_AC_CHOICES = [
        (CVSS_AC_LOW, "Low (L)"), (CVSS_AC_HIGH, "High (H)")
    ]

    # Privileges Required
    CVSS_PR_NONE = "N"
    CVSS_PR_LOW = "L"
    CVSS_PR_HIGH = "H"
    CVSS_PR_CHOICES = [
        (CVSS_PR_NONE, "None (N)"), (CVSS_PR_LOW, "Low (L)"), (CVSS_PR_HIGH, "High (H)")
    ]

    # User Interaction
    CVSS_UI_NONE = "N"
    CVSS_UI_REQUIRED = "R"
    CVSS_UI_CHOICES = [
        (CVSS_UI_NONE, "None (N)"), (CVSS_UI_REQUIRED, "Required (R)")
    ]

    # Scope
    CVSS_S_UNCHANGED = "U"
    CVSS_S_CHANGED = "C"
    CVSS_S_CHOICES = [
        (CVSS_S_UNCHANGED, "Unchanged (U)"), (CVSS_S_CHANGED, "Changed (C)")
    ]
    # Confidentiality
    CVSS_C_NONE = "N"
    CVSS_C_LOW = "L"
    CVSS_C_HIGH = "H"
    CVSS_C_CHOICES = [
        (CVSS_C_NONE, "None (N)"), (CVSS_C_LOW, "Low (L)"), (CVSS_C_HIGH, "High (H)")
    ]

    # Integrity
    CVSS_I_NONE = "N"
    CVSS_I_LOW = "L"
    CVSS_I_HIGH = "H"
    CVSS_I_CHOICES = [
        (CVSS_I_NONE, "None (N)"), (CVSS_I_LOW, "Low (L)"), (CVSS_I_HIGH, "High (H)")
    ]

    # Availability
    CVSS_A_NONE = "N"
    CVSS_A_LOW = "L"
    CVSS_A_HIGH = "H"
    CVSS_A_CHOICES = [
        (CVSS_A_NONE, "None (N)"), (CVSS_A_LOW, "Low (L)"), (CVSS_A_HIGH, "High (H)")
    ]

    cvss_av = models.CharField(max_length=3, choices=CVSS_AV_CHOICES, blank=True, null=True)
    cvss_ac = models.CharField(max_length=3, choices=CVSS_AC_CHOICES, blank=True, null=True)
    cvss_pr = models.CharField(max_length=3, choices=CVSS_PR_CHOICES, blank=True, null=True)
    cvss_ui = models.CharField(max_length=3, choices=CVSS_UI_CHOICES, blank=True, null=True)
    cvss_s = models.CharField(max_length=3, choices=CVSS_S_CHOICES, blank=True, null=True)
    cvss_c = models.CharField(max_length=3, choices=CVSS_C_CHOICES, blank=True, null=True)
    cvss_i = models.CharField(max_length=3, choices=CVSS_I_CHOICES, blank=True, null=True)
    cvss_a = models.CharField(max_length=3, choices=CVSS_A_CHOICES, blank=True, null=True)

    class Meta:
        abstract = True

    def cvss_get_vector_string(self):
        values = ["CVSS:3.1", "AV:%s" % self.cvss_av, "AC:%s" % self.cvss_ac, "PR:%s" % self.cvss_pr,
            "UI:%s" % self.cvss_ui, "S:%s" % self.cvss_s, "C:%s" % self.cvss_c, "I:%s" % self.cvss_i,
            "A:%s" % self.cvss_a
        ]
        return "/".join(values)

    def cvss_get_base_score(self):
        try:
            return cvss.CVSS3(self.cvss_get_vector_string()).scores()[0]
        except:
            return None


def project_pocs_path(instance, filename):
    return "uploads/proofs/projects/%s/%s" % (instance.pk, filename)


class Vulnerability(BaseCVSS, VulnmanProjectModel):
    SEVERITY_COLOR_CRITICAL = "#9c1720"
    SEVERITY_COLOR_HIGH = "#d13c0f"
    SEVERITY_COLOR_MEDIUM = "#e8971e"
    SEVERITY_COLOR_LOW = "#2075f5"
    SEVERITY_COLOR_INFORMATIONAL = "#059D1D"
    SEVERITY_COLORS = {
        "Critical": SEVERITY_COLOR_CRITICAL,
        "High": SEVERITY_COLOR_HIGH,
        "Medium": SEVERITY_COLOR_MEDIUM,
        "Low": SEVERITY_COLOR_LOW,
        "Informational": SEVERITY_COLOR_INFORMATIONAL
    }

    STATUS_OPEN = 0
    STATUS_FIXED = 1
    STATUS_TO_REVIEW = 2

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_TO_REVIEW, "To Review"),
        (STATUS_FIXED, "Fixed")
    ]

    template = models.ForeignKey('findings.Template', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    cve_id = models.CharField(max_length=28, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_OPEN)
    severity = models.PositiveIntegerField(choices=SEVERITY_CHOICES, blank=True, null=True)
    # generic assets
    asset_type = models.CharField(max_length=64, choices=ASSET_TYPES_CHOICES, default=WebApplication.ASSET_TYPE)
    asset_webapp = models.ForeignKey('assets.WebApplication', on_delete=models.CASCADE, null=True, blank=True)
    asset_webrequest = models.ForeignKey('assets.WebRequest', on_delete=models.CASCADE, null=True, blank=True)
    asset_host = models.ForeignKey('assets.Host', on_delete=models.CASCADE, null=True, blank=True)
    asset_service = models.ForeignKey('assets.Service', on_delete=models.CASCADE, null=True, blank=True)

    auth_required = models.BooleanField(default=False)
    user_account = models.ForeignKey('findings.UserAccount', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.template.name

    def get_severity(self):
        if self.severity:
            return self.severity
        return self.template.severity

    def get_severity_color(self):
        if not self.severity:
            return ""
        return self.SEVERITY_COLORS[self.get_severity_display()]

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
        elif self.asset_service:
            return self.asset_service

    class Meta:
        ordering = ['-severity']
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

    def __str__(self):
        return self.name


class TextProof(Proof):
    text = models.TextField(help_text="Markdown supported!")

    def get_absolute_delete_url(self):
        return reverse_lazy(
            "projects:findings:text-proof-delete",
            kwargs={"pk": self.pk})

class ImageProof(Proof):
    caption = models.CharField(max_length=128, blank=True, null=True)
    image = models.ImageField(max_length=256, upload_to=project_pocs_path)

    def base64_encoded_image(self):
        with open(self.image.path, "rb") as image_f:
            encoded = base64.b64encode(image_f.read())
            return "data:image/png;base64, %s" % encoded.decode()

    def get_absolute_delete_url(self):
        return reverse_lazy(
            "projects:findings:image-proof-delete",
            kwargs={"pk": self.pk})


class Template(BaseVulnerability):
    vulnerability_id = models.CharField(max_length=256, unique=True)

    class Meta:
        ordering = ['vulnerability_id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('findings:template-detail', kwargs={'pk': self.pk})

    def get_risk_level(self):
        return self.get_severity_display()


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


@receiver(models.signals.post_delete, sender=ImageProof)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=ImageProof)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
