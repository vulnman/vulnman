from django.db import models
from django.urls import reverse_lazy
from apps.assets.models.base import BaseAsset


class WebRequest(BaseAsset):
    ASSET_TYPE = "webrequest"
    ASSET_TYPE_CHOICE = (ASSET_TYPE, "Web Request")

    web_app = models.ForeignKey('assets.WebApplication', on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    parameter = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.url

    @property
    def name(self):
        return self.url

    class Meta:
        verbose_name = "Web Request"
        verbose_name_plural = "Web Requests"
        unique_together = [
            ("web_app", "url", "parameter")
        ]

    def get_absolute_delete_url(self):
        return reverse_lazy(
            "projects:assets:webrequest-delete",
            kwargs={"pk": self.pk})
