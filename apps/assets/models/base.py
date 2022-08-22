from django.db import models
from vulnman.models import VulnmanProjectModel
from apps.findings.models import Vulnerability


class BaseAsset(VulnmanProjectModel):
    description = models.TextField(blank=True)
    hide_from_report = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def asset_type(self):
        return self._meta.verbose_name

    def vulnerabilities_for_asset(self):
        return Vulnerability.objects.filter(asset_type=self.ASSET_TYPE, object_id=self.pk)
