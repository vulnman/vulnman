from django.db import models
from apps.assets.models.base import BaseAsset


class WebRequest(BaseAsset):
    web_app = models.ForeignKey('apps.assets.WebApplication', on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    parameter = models.CharField(max_length=255, blank=True)

