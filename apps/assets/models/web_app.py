from django.db import models
from apps.assets.models.base import BaseAsset


class WebApplication(BaseAsset):
    name = models.CharField(max_length=256)
    base_url = models.URLField()
