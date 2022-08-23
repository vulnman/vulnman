from django.db import models
from django.urls import reverse
from apps.assets.models.base import BaseAsset


class WebURL(BaseAsset):
    ASSET_TYPE = "weburl"
    ASSET_TYPE_CHOICE = (ASSET_TYPE, "URL")

    webapp = models.ForeignKey('assets.WebApplication', on_delete=models.CASCADE)
    path = models.CharField(max_length=512)

    def __str__(self):
        return self.path
