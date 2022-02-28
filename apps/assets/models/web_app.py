from django.db import models
from apps.assets.models.base import BaseAsset


class WebApplication(BaseAsset):
<<<<<<< HEAD
=======
    ASSET_TYPE = "webapplication"
    ASSET_TYPE_CHOICE = (ASSET_TYPE, "Web Application")

>>>>>>> origin/dev
    name = models.CharField(max_length=256)
    base_url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Web Application"
        verbose_name_plural = "Web Applications"