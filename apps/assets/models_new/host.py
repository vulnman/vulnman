from django.db import models
from apps.assets.models.base import BaseAsset


class Host(BaseAsset):
    ip = models.GenericIPAddressField()
    operating_system = models.CharField(max_length=256, blank=True)
    is_online = models.BooleanField(default=True)

    class Meta:
        ordering = ['ip']
        unique_together = [
            ('project', 'ip')
        ]

class Hostname(BaseAsset):
    name = models.CharField(max_length=256)
    host = models.ForeignKey(Host, on_delete=models.PROTECT)

    class Meta:
        unique_together = [
            ('project', 'name')
        ]
