from django.db import models
from django.urls import reverse_lazy
from apps.assets.models.base import BaseAsset


class Network(BaseAsset):
    ASSET_TYPE = "network"
    ASSET_TYPE_CHOICE = (ASSET_TYPE, "Network")

    name = models.CharField(max_length=64)
    start_ip = models.GenericIPAddressField(verbose_name="Start-IP")
    network_mask = models.IntegerField()
    vlan = models.PositiveIntegerField()

    class Meta:
        unique_together = [
            ('project', 'name')
        ]

    def __str__(self):
        return self.name

    def get_network_range(self):
        return "{start_ip}/{netmask}".format(start_ip=self.start_ip, netmask=self.network_mask)

    def get_absolute_delete_url(self):
        return reverse_lazy(
            "projects:assets:host-delete", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse_lazy("projects:assets:host-detail", kwargs={"pk": self.pk})
