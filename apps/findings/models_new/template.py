from django.db import models
from apps.findings.models.base import BaseVulnerability


class VulnerabilityTemplate(BaseVulnerability):
    vulnerability_id = models.CharField(max_length=256, unique=True)

    class Meta:
        ordering = ['vulnerability_id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('findings:template-detail', kwargs={'pk': self.pk})

    def get_risk_level(self):
        return self.vulnerability_set.first().get_severities()[0]
