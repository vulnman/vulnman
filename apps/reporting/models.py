from django.db import models
from django.urls import reverse_lazy
from django.conf import settings
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
    language = models.CharField(choices=settings.LANGUAGES, default="en", max_length=6)

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
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="created_reportinformation_set",
        null=True, blank=True)
    evaluation = models.TextField(null=True, blank=True)
    recommendation = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
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
