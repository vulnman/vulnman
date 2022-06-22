import base64
from django.db import models
from django.urls import reverse_lazy
from django.conf import settings
from vulnman.models import VulnmanModel


class Vulnerability(models.Model):
    STATUS_OPEN = 0
    STATUS_CLOSED = 1

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_CLOSED, "Closed")
    ]

    SEVERITY_INFORMATIONAL = 0
    SEVERITY_LOW = 1
    SEVERITY_MEDIUM = 2
    SEVERITY_HIGH = 3
    SEVERITY_CRITICAL = 4

    SEVERITY_CHOICES = [
        (SEVERITY_CRITICAL, "Critical"),
        (SEVERITY_HIGH, "High"),
        (SEVERITY_MEDIUM, "Medium"),
        (SEVERITY_LOW, "Low"),
        (SEVERITY_INFORMATIONAL, "Informational")
    ]

    template = models.ForeignKey('findings.Template', on_delete=models.CASCADE, related_name="resp_vulnerability_set")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_OPEN)
    severity = models.PositiveIntegerField(choices=SEVERITY_CHOICES, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resp_vulnerability_set")
    vendor = models.CharField(max_length=128)
    vendor_homepage = models.URLField()
    vendor_email = models.EmailField(null=True)
    affected_product = models.CharField(max_length=256)
    affected_versions = models.CharField(max_length=256)
    fixed_version = models.CharField(max_length=100, null=True, blank=True)
    cve_id = models.CharField(max_length=32, null=True, blank=True, verbose_name="CVE-ID")
    cve_request_id = models.CharField(max_length=32, null=True, blank=True, verbose_name="CVE Request ID")
    is_published = models.BooleanField(default=False)
    is_fixed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_severity(self):
        if self.severity:
            return self.severity
        return self.template.severity

    def get_absolute_url(self):
        return reverse_lazy("responsible_disc:vulnerability-detail", kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy("responsible_disc:vulnerability-delete", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            VulnerabilityLog.objects.create(action=VulnerabilityLog.ACTION_VULNERABILITY_CREATION,
                                            vulnerability=self, message="Vulnerability created in vulnman")
            return
        return super().save(*args, **kwargs)

    @property
    def proofs(self):
        proofs = list(self.textproof_set.all()) + list(self.imageproof_set.all())
        proofs.sort(key=lambda proof: proof.order or 0)
        return proofs

    def get_public_timeline(self):
        return self.vulnerabilitylog_set.filter(~models.Q(action=VulnerabilityLog.ACTION_INTERNAL_LOG))

    def get_timeline(self):
        return self.vulnerabilitylog_set.all()

    class Meta:
        ordering = ["-date_created"]


def get_proof_path(instance, filename):
    return "uploads/responsible_disclosure/%s/%s/%s" % (instance.user.pk, instance.vulnerability.pk, filename)


class Proof(models.Model):
    # TODO: some of duplicate code stuff is flying around here
    # Improve this
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(null=True)
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class TextProof(Proof):
    text = models.TextField(help_text="Markdown supported!")

    def get_absolute_delete_url(self):
        return reverse_lazy("responsible_disc:text-proof-delete", kwargs={"pk": self.pk})


class ImageProof(Proof):
    caption = models.CharField(max_length=128, blank=True, null=True)
    image = models.ImageField(max_length=256, upload_to=get_proof_path)

    def base64_encoded_image(self):
        with open(self.image.path, "rb") as image_f:
            encoded = base64.b64encode(image_f.read())
            return "data:image/png;base64, %s" % encoded.decode()

    def get_absolute_delete_url(self):
        return reverse_lazy("responsible_disc:image-proof-delete", kwargs={"pk": self.pk})


class VulnerabilityLog(VulnmanModel):
    ACTION_VULNERABILITY_CREATION = 0
    ACTION_VENDOR_NOTIFIED = 1
    ACTION_VENDOR_COMMUNICATION = 2
    ACTION_VENDOR_ANNOUNCE_FIXED = 3
    ACTION_FIX_CONFIRMED = 4
    ACTION_PUBLISHED = 5
    ACTION_INTERNAL_LOG = 100

    ACTION_CHOICES = [
        (ACTION_VENDOR_NOTIFIED, "Notified vendor"),
        (ACTION_VULNERABILITY_CREATION, "Vulnerability found"),
        (ACTION_VENDOR_ANNOUNCE_FIXED, "Vendor announces fix"),
        (ACTION_VENDOR_COMMUNICATION, "Communication with vendor"),
        (ACTION_FIX_CONFIRMED, "Fix confirmed"),
        (ACTION_PUBLISHED, "Advisory published"),
        (ACTION_INTERNAL_LOG, "Custom Internal Log")
    ]
    vulnerability = models.ForeignKey('responsible_disc.Vulnerability', on_delete=models.CASCADE)
    custom_date = models.DateTimeField(null=True, blank=True)
    action = models.PositiveIntegerField(choices=ACTION_CHOICES)
    message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["date_created"]


class VulnerabilityComment(VulnmanModel):
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        ordering = ["date_created"]
