from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Report(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    revision = models.CharField(max_length=6, default="0.1", help_text="The reports are ordered by revisions")
    date_created = models.DateTimeField(auto_now_add=True)
    custom_title = models.CharField(max_length=64, help_text="Overwrite Project Title", null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changes = models.CharField(max_length=128)
    latex_source = models.TextField(null=True, blank=True)
    pdf_source = models.BinaryField(null=True, blank=True)
    is_draft = models.BooleanField(default=False)
    include_watermark = models.BooleanField(default=True)

    class Meta:
        unique_together = [('project', 'revision')]
        ordering = ["revision"]

    def __str__(self):
        return self.revision
