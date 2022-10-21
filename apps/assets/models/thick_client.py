from django.db import models
from django.urls import reverse_lazy
from django.contrib.contenttypes.fields import GenericRelation
from apps.assets.models.base import BaseAsset


class ThickClient(BaseAsset):
    ASSET_TYPE = "thick-client"
    ASSET_TYPE_CHOICE = (ASSET_TYPE, "Thick-Client")

    name = models.CharField(max_length=128)
    programming_language = models.CharField(max_length=32, null=True, blank=True)
    version = models.CharField(max_length=16, blank=True, null=True)
    operating_system = models.CharField(max_length=256, blank=True, verbose_name="Operating System")
    environment = models.PositiveIntegerField(choices=BaseAsset.ENVIRONMENT_CHOICES,
                                              default=BaseAsset.ENVIRONMENT_UNKNOWN)
    vulnerabilities = GenericRelation('findings.Vulnerability')

    class Meta:
        ordering = ['-date_updated']
        unique_together = [
            ('project', 'name')
        ]

    def __str__(self):
        return self.name

    def get_absolute_delete_url(self):
        return reverse_lazy("projects:assets:thick-client-delete", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse_lazy("projects:assets:thick-client-detail", kwargs={"pk": self.pk})
