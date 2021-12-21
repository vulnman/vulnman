from django.db import models
from django.urls import reverse_lazy
from django.core import signing
from django.utils import timezone
from django.contrib.auth.models import User
from uuid import uuid4
from vulnman.models import VulnmanProjectModel


class Report(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    revision = models.CharField(max_length=6, default="0.1", help_text="The reports are ordered by revisions")
    date_created = models.DateTimeField(auto_now_add=True)
    custom_title = models.CharField(max_length=64, help_text="Overwrite Project Title", null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changes = models.CharField(max_length=128)
    raw_source = models.TextField(null=True, blank=True)
    pdf_source = models.BinaryField(null=True, blank=True)
    is_draft = models.BooleanField(default=False)
    include_watermark = models.BooleanField(default=True)

    class Meta:
        unique_together = [('project', 'revision')]
        ordering = ["revision"]

    def __str__(self):
        return self.revision

    def get_absolute_delete_url(self):
        return reverse_lazy('projects:reporting:report-delete', kwargs={'pk': self.pk})


class ReportShareToken(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    share_token = models.CharField(max_length=512, null=True, blank=True)
    date_expires = models.DateTimeField()

    def save(self, *args, **kwargs):
        # save instance twice, because we need the ID which is set by the database!
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
            return not cls.objects.filter(pk=value.get("report"), date_expires__gt=timezone.now()).exists()
        return True


class ReportSection(VulnmanProjectModel):
    name = models.CharField(max_length=64)
    text = models.TextField(help_text="Markdown supported!")
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    order = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = [("report", "order")]
        verbose_name_plural = "Report Sections"
        verbose_name = "Report Section"
