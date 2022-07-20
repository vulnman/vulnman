from django.db import models
from vulnman.models import VulnmanProjectModel


class BaseAsset(VulnmanProjectModel):
    description = models.TextField(blank=True)
    hide_from_report = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def asset_type(self):
        return self._meta.verbose_name
