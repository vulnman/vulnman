from django.db import models
from apps.assets.models.base import BaseAsset


class Host(BaseAsset):
<<<<<<< HEAD
    ip = models.GenericIPAddressField()
    operating_system = models.CharField(max_length=256, blank=True)
    is_online = models.BooleanField(default=True)
=======
    ASSET_TYPE = "host"
    ASSET_TYPE_CHOICE = (ASSET_TYPE, "Host")

    ACCESSIBILITY_NOT_TESTED = 0
    ACCESSIBILITY_ACCESSIBLE = 1
    ACCESSIBILITY_NOT_ACCESSIBLE = 2

    ACCESSIBILITY_CHOICES = [
        (ACCESSIBILITY_ACCESSIBLE, "Accessible"),
        (ACCESSIBILITY_NOT_ACCESSIBLE, "Not Accessible"),
        (ACCESSIBILITY_NOT_TESTED, "Not Tested")
    ]

    ip = models.GenericIPAddressField()
    operating_system = models.CharField(max_length=256, blank=True)
    accessibility = models.IntegerField(choices=ACCESSIBILITY_CHOICES, default=ACCESSIBILITY_NOT_TESTED)
    dns = models.CharField(max_length=256, null=True, blank=True)
>>>>>>> origin/dev

    class Meta:
        ordering = ['ip']
        unique_together = [
            ('project', 'ip')
        ]
<<<<<<< HEAD

class Hostname(BaseAsset):
    name = models.CharField(max_length=256)
    host = models.ForeignKey(Host, on_delete=models.PROTECT)

    class Meta:
        unique_together = [
            ('project', 'name')
        ]
=======
>>>>>>> origin/dev
