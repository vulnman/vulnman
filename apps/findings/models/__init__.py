import os
import base64
from uuid import uuid4
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from vulnman.models import VulnmanModel, VulnmanProjectModel
from apps.findings import querysets
from apps.findings.models.scores import OWASPScore, CVSScore


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


def get_severity_by_int(value):
    for sev in SEVERITY_CHOICES:
        if sev[0] == value:
            return sev[1]
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

    class Meta:
        abstract = True


def project_pocs_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid4(), ext)
    return "uploads/projects/%s/proofs/%s" % (instance.vulnerability.project.pk, filename)


class Vulnerability(VulnmanProjectModel):
    SEVERITY_CRITICAL = 4
    SEVERITY_HIGH = 3
    SEVERITY_MEDIUM = 2
    SEVERITY_LOW = 1
    SEVERITY_INFORMATIONAL = 0
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
    ASSET_TYPES_CHOICES = [
        ("webapplication", "Web Application"),
        ("host", "Host"),
        ("service", "Service")
    ]

    objects = querysets.VulnerabilityManager.from_queryset(querysets.VulnerabilityQuerySet)()
    template = models.ForeignKey('findings.Template', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    cve_id = models.CharField(max_length=28, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_OPEN)
    severity = models.PositiveIntegerField(choices=SEVERITY_CHOICES, blank=True, null=True)
    date_retested = models.DateField(null=True, blank=True)
    # generic assets
    asset_type = models.CharField(max_length=64, choices=ASSET_TYPES_CHOICES, default="webapplication")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    asset = GenericForeignKey("content_type", "object_id")
    auth_required = models.BooleanField(default=False)  # not yet used
    user_account = models.ForeignKey('findings.UserAccount', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.template.name

    def get_severity(self):
        if self.severity:
            return self.severity
        return self.template.severity

    def save(self, *args, **kwargs):
        if self.status == self.STATUS_FIXED and not self.date_retested:
            self.date_retested = timezone.now()
        return super().save(*args, **kwargs)

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

    class Meta:
        ordering = ['-severity']
        verbose_name_plural = "Vulnerabilities"
        verbose_name = "Vulnerability"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


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
    objects = querysets.TemplateQuerySet.as_manager()
    vulnerability_id = models.CharField(max_length=256, unique=True)
    category = models.ForeignKey(
        VulnerabilityCategory, on_delete=models.PROTECT, null=True)

    class Meta:
        ordering = ['vulnerability_id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('findings:template-detail', kwargs={'pk': self.pk})

    def get_highest_severity_for_project(self, project):
        most_critical_vulnerability = project.vulnerability_set.filter(template=self).first()
        return most_critical_vulnerability


class Reference(VulnmanModel):
    name = models.CharField(max_length=255)
    template = models.ForeignKey(
        Template, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "References"
        verbose_name = "Reference"


class UserAccount(VulnmanProjectModel):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=512, blank=True, null=True)
    role = models.CharField(max_length=128, blank=True, null=True)
    account_compromised = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_absolute_delete_url(self):
        return reverse_lazy("projects:findings:user-account-delete", kwargs={"pk": self.pk})


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
