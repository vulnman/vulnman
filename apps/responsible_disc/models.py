import base64
from django.db import models
from django.contrib.auth.models import User


class Vulnerability(models.Model):
    STATUS_OPEN = 0
    STATUS_FIXED = 1
    STATUS_VENDOR_NOTIFIED = 2
    STATUS_VENDOR_ACK = 3

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_VENDOR_NOTIFIED, "Vendor Notified"),
        (STATUS_VENDOR_ACK, "Vendor Acknowledged"),
        (STATUS_FIXED, "Fixed"),
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resp_vulnerability_set")
    vendor = models.CharField(max_length=128)
    vendor_homepage = models.URLField()
    affected_product = models.CharField(max_length=256)
    affected_versions = models.CharField(max_length=256)
    fixed_version = models.CharField(max_length=100, null=True, blank=True)
    cve_id = models.CharField(max_length=32, null=True, blank=True)
    cve_request_id = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_severity(self):
        if self.severity:
            return self.severity
        return self.template.severity


def get_proof_path(instance, filename):
    return "uploads/responsible_disclosure/%s/%s/%s" % (instance.user.pk, instance.pk, filename)


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


class ImageProof(Proof):
    caption = models.CharField(max_length=128, blank=True, null=True)
    image = models.ImageField(max_length=256, upload_to=get_proof_path)

    def base64_encoded_image(self):
        with open(self.image.path, "rb") as image_f:
            encoded = base64.b64encode(image_f.read())
            return "data:image/png;base64, %s" % encoded.decode()

