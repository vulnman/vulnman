from django.db import models
from django.urls import reverse_lazy
from django.core import signing
from django.utils import timezone
from django.contrib.auth.models import User
from uuid import uuid4
from vulnman.models import VulnmanProjectModel


class PentestReport(VulnmanProjectModel):
    REPORT_TYPE_DRAFT = "draft"
    REPORT_TYPE_RELEASE = "release"

    REPORT_TYPE_CHOICES = [
        (REPORT_TYPE_DRAFT, "Draft"), (REPORT_TYPE_RELEASE, "Release")
    ]
    name = models.CharField(max_length=128)
    report_type = models.CharField(max_length=16, choices=REPORT_TYPE_CHOICES)
    raw_source = models.TextField(null=True, blank=True)
    pdf_source = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.get_report_type_display()

    @property
    def version(self):
        return "0.1"

    def get_absolute_delete_url(self):
        return reverse_lazy('projects:reporting:report-delete', kwargs={
            'pk': self.pk})

    class Meta:
        ordering = ["-date_created"]


class ReportInformation(VulnmanProjectModel):
    REPORT_DEFAULT_TITLE = "Vulnerability Report"
    project = models.OneToOneField("projects.Project", on_delete=models.CASCADE)
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="created_reportinformation_set",
        null=True, blank=True)
    evaluation = models.TextField(null=True, blank=True)
    recommendation = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="reportinformation_set")
    title = models.CharField(max_length=256, null=True, blank=True)

    def get_report_title(self):
        if self.title:
            return self.title
        return self.REPORT_DEFAULT_TITLE


# class ReportVersion(VulnmanProjectModel):
#    report = models.ForeignKey(PentestReport, on_delete=models.CASCADE)
#    version = models.FloatField()
#    change = models.CharField(choices=[], max_length=512)
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    date = models.DateField()


class ReportShareToken(models.Model):
    # TODO: not in use! legacy
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    report = models.OneToOneField(PentestReport, on_delete=models.CASCADE)
    share_token = models.CharField(max_length=512, null=True, blank=True)
    date_expires = models.DateTimeField()

    def save(self, *args, **kwargs):
        # save instance twice, because we need the ID which is set by the
        # database!
        super().save(*args, **kwargs)
        if not self.share_token:
            self._create_token()
            self.save(update_fields=["share_token"])

    def _create_token(self):
        signer = signing.TimestampSigner()
        self.share_token = signer.sign_object({"report": str(self.uuid)})

    @classmethod
    def is_expired(cls, token):
        signer = signing.TimestampSigner()
        try:
            value = signer.unsign_object(token)
        except signing.SignatureExpired:
            return True
        if value:
            return not cls.objects.filter(
                pk=value.get("report"), date_expires__gt=timezone.now()).exists()
        return True
