from django.db import models
from vulnman.models import VulnmanProjectModel


class BaseAsset(VulnmanProjectModel):
    description = models.TextField(blank=True)
    in_pentest_report = models.BooleanField(default=True, blank=True)

    class Meta:
        abstract = True
