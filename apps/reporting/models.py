from django.db import models
from django.urls import reverse_lazy
from django.conf import settings
from vulnman.models import VulnmanProjectModel


def get_report_templates():
    choices = []
    for template in settings.REPORT_TEMPLATES.keys():
        choices.append((template, template))
    return choices


class Report(VulnmanProjectModel):
    REPORT_DEFAULT_TITLE = "Vulnerability Report"
    REPORT_TYPE_PDF = 0
    REPORT_TYPE_JSON = 1

    REPORT_TYPE_CHOICES = [
        (REPORT_TYPE_PDF, "PDF"),
        (REPORT_TYPE_JSON, "JSON")
    ]
    REPORT_TYPE_CONTENT_TYPES = {
        REPORT_TYPE_PDF: "application/pdf",
        REPORT_TYPE_JSON: "application/json"
    }

    name = models.CharField(max_length=128, default="Report")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="created_report_set",
        null=True, blank=True)
    evaluation = models.TextField(null=True, blank=True)
    recommendation = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="report_set")
    title = models.CharField(max_length=256, null=True, blank=True)
    language = models.CharField(choices=settings.LANGUAGES, default="en", max_length=6)
    template = models.CharField(choices=get_report_templates(), default="default", max_length=64)
    report_type = models.PositiveIntegerField(choices=REPORT_TYPE_CHOICES, default=0)

    def get_report_title(self):
        if self.title:
            return self.title
        return self.REPORT_DEFAULT_TITLE

    def get_absolute_url(self):
        return reverse_lazy("projects:reporting:report-detail", kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy("projects:reporting:report-delete", kwargs={"pk": self.pk})

    def get_next_minor_version(self):
        if not self.reportversion_set.count():
            return "0.1"
        return self.reportversion_set.first().version + 0.1

    def get_current_version(self):
        if not self.reportversion_set.count():
            return "0.1"
        return self.reportversion_set.first().version

    class Meta:
        ordering = ["-date_created"]


class ReportRelease(VulnmanProjectModel):
    RELEASE_TYPE_DRAFT = "draft"
    RELEASE_TYPE_RELEASE = "release"

    RELEASE_TYPE_CHOICES = [
        (RELEASE_TYPE_DRAFT, "Draft"),
        (RELEASE_TYPE_RELEASE, "Release")
    ]
    name = models.CharField(max_length=128)
    release_type = models.CharField(max_length=16, choices=RELEASE_TYPE_CHOICES)
    raw_source = models.TextField(null=True, blank=True)
    compiled_source = models.BinaryField(null=True, blank=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    work_in_progress = models.BooleanField(default=False)
    task_id = models.CharField(max_length=512, null=True, blank=True)

    def get_absolute_url(self):
        return reverse_lazy("projects:reporting:report-release-detail", kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy("projects:reporting:report-release-delete", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-date_created"]


class ReportVersion(VulnmanProjectModel):
    REPORT_CHANGE_CHOICES = [
        (0, "Report created"),
        (5, "Added vulnerabilities"),
        (10, "Fixed typo"),
        (20, "Report finalized")
    ]

    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    version = models.FloatField()
    change = models.PositiveIntegerField(choices=REPORT_CHANGE_CHOICES)
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, related_name="user_set")
    date = models.DateField()

    class Meta:
        ordering = ["version"]
        unique_together = [
            ("report", "version")
        ]
