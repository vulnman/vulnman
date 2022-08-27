from django.db import models
from vulnman.models import VulnmanProjectModel
from apps.findings.models import Vulnerability


class BaseAsset(VulnmanProjectModel):
    description = models.TextField(blank=True)
    hide_from_report = models.BooleanField(default=False)

    ACCESSIBILITY_NOT_TESTED = 0
    ACCESSIBILITY_ACCESSIBLE = 1
    ACCESSIBILITY_NOT_ACCESSIBLE = 2

    ACCESSIBILITY_CHOICES = [
        (ACCESSIBILITY_ACCESSIBLE, "Accessible"),
        (ACCESSIBILITY_NOT_ACCESSIBLE, "Not Accessible"),
        (ACCESSIBILITY_NOT_TESTED, "Not Tested")
    ]

    ENVIRONMENT_UNKNOWN = 0
    ENVIRONMENT_TESTING = 1
    ENVIRONMENT_PRODUCTION = 2
    ENVIRONMENT_STAGING = 3
    ENVIRONMENT_DEVELOPMENT = 4

    ENVIRONMENT_CHOICES = [
        (ENVIRONMENT_UNKNOWN, "Unknown"),
        (ENVIRONMENT_PRODUCTION, "Production"),
        (ENVIRONMENT_TESTING, "Testing"),
        (ENVIRONMENT_DEVELOPMENT, "Development"),
        (ENVIRONMENT_STAGING, "Staging")
    ]

    accessibility = models.IntegerField(choices=ACCESSIBILITY_CHOICES, default=ACCESSIBILITY_NOT_TESTED)

    class Meta:
        abstract = True

    @property
    def asset_type(self):
        return self._meta.verbose_name

    def vulnerabilities_for_asset(self):
        return Vulnerability.objects.filter(asset_type=self.ASSET_TYPE, object_id=self.pk)
