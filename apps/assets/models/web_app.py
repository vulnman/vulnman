from django.db import models
from django.urls import reverse_lazy
from apps.assets.models.base import BaseAsset


class WebApplication(BaseAsset):
    ASSET_TYPE = "webapplication"
    ASSET_TYPE_CHOICE = (ASSET_TYPE, "Web Application")

    name = models.CharField(max_length=256)
    base_url = models.URLField()
    environment = models.PositiveIntegerField(choices=BaseAsset.ENVIRONMENT_CHOICES,
                                              default=BaseAsset.ENVIRONMENT_UNKNOWN)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Web Application"
        verbose_name_plural = "Web Applications"
        ordering = ["-date_created"]

    def get_absolute_delete_url(self):
        return reverse_lazy(
            "projects:assets:webapp-delete",
            kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse_lazy(
            "projects:assets:webapp-detail", kwargs={"pk": self.pk})
