from django.db import models
from django.urls import reverse_lazy
from apps.assets.models.base import BaseAsset


class Host(BaseAsset):
    ASSET_TYPE = "host"
    ASSET_TYPE_CHOICE = (ASSET_TYPE, "Host")

    ip = models.GenericIPAddressField(verbose_name="IP")
    operating_system = models.CharField(max_length=256, blank=True, verbose_name="Operating System")
    dns = models.CharField(max_length=256, null=True, blank=True, verbose_name="DNS")

    class Meta:
        ordering = ['ip']
        unique_together = [
            ('project', 'ip')
        ]

    def __str__(self):
        if self.dns:
            return "%s (%s)" % (self.dns, self.ip)
        return self.ip

    @property
    def name(self):
        return self.__str__()

    def get_absolute_delete_url(self):
        return reverse_lazy(
            "projects:assets:host-delete", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse_lazy("projects:assets:host-detail", kwargs={"pk": self.pk})
