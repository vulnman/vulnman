from django.db import models
from django.urls import reverse_lazy
from django.conf import settings
from vulnman.models import VulnmanProjectModel
from django.utils.module_loading import import_string


def get_report_templates():
    choices = []
    for template in settings.REPORT_TEMPLATES.keys():
        choices.append((template, template))
    return choices


class Report(VulnmanProjectModel):
    REPORT_DEFAULT_TITLE = "Pentest Report"
    REPORT_VARIANT_PENTEST_REPORT = 0
    REPORT_VARIANT_PENTEST_CSV = 1

    REPORT_VARIANT_CHOICES = [
        (REPORT_VARIANT_PENTEST_REPORT, "Pentest Report"),
        (REPORT_VARIANT_PENTEST_CSV, "Pentest CSV")
    ]

    REPORT_VARIANT_CONTENT_TYPES = {
        REPORT_VARIANT_PENTEST_REPORT: "application/pdf",
        REPORT_VARIANT_PENTEST_CSV: "text/csv"
    }

    REPORT_VARIANT_IMPORTS = {
        REPORT_VARIANT_PENTEST_REPORT: "pentest_report.Report",
        REPORT_VARIANT_PENTEST_CSV: "csv.Report",
    }

    REPORT_VARIANT_EXTENSIONS = {
        REPORT_VARIANT_PENTEST_REPORT: "pdf",
        REPORT_VARIANT_PENTEST_CSV: "csv"
    }

    name = models.CharField(max_length=128, default="Pentest Report")
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
    report_variant = models.PositiveIntegerField(choices=REPORT_VARIANT_CHOICES, default=REPORT_VARIANT_PENTEST_REPORT)

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

    def get_report_content_type(self):
        return self.REPORT_VARIANT_CONTENT_TYPES.get(self.report_variant, "application/octet-stream")

    def get_report_file_extension(self):
        return self.REPORT_VARIANT_EXTENSIONS.get(self.report_variant, "txt")

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

    def get_report_variant(self):
        imp_string = "%s.%s" % (settings.REPORT_TEMPLATES.get(self.report.template, "default"),
                                self.report.REPORT_VARIANT_IMPORTS.get(self.report.report_variant))
        ReportClass = import_string(imp_string)
        return ReportClass(self)

    class Meta:
        ordering = ["-date_created"]


class ReportVersion(VulnmanProjectModel):
    REPORT_CHANGE_REPORT_CREATED = 0
    REPORT_CHANGE_ADDED_VULNERABILITIES = 5
    REPORT_CHANGE_FIXED_TYPO = 10
    REPORT_CHANGE_REPORT_FINALIZED = 20

    REPORT_CHANGE_CHOICES = [
        (REPORT_CHANGE_REPORT_CREATED, "Report created"),
        (REPORT_CHANGE_ADDED_VULNERABILITIES, "Added vulnerabilities"),
        (REPORT_CHANGE_FIXED_TYPO, "Fixed typo"),
        (REPORT_CHANGE_REPORT_FINALIZED, "Report finalized")
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

    def get_absolute_delete_url(self):
        return reverse_lazy("projects:reporting:version-delete", kwargs={"pk": self.pk})
