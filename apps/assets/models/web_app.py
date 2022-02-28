from django.db import models
from apps.assets.models.base import BaseAsset


class WebApplication(BaseAsset):
    name = models.CharField(max_length=256)
    base_url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Web Application"
        verbose_name_plural = "Web Applications"