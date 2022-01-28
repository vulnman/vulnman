from django.db import models
from apps.assets.models.base import BaseAsset

PROTOCOL_CHOICES = [
    ("tcp", "TCP"),
    ("udp", "UDP"),
]


STATE_CHOICES = [
    ("closed", "Closed"),
    ("open", "Open"),
    ("filtered", "Filtered")
]


class Service(BaseAsset):
    port = models.PositiveIntegerField(validators=[MaxValueValidator(65535)], blank=True, null=True)
    host = models.ForeignKey('apps.assets.Host', on_delete=models.PROTECT)
    name = models.CharField(max_length=64, blank=True)
    protocol = models.CharField(max_length=12, default="tcp", choices=PROTOCOL_CHOICES)
    state = models.CharField(max_length=24, default="closed", choices=STATE_CHOICES)
    banner = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = [
            ('project', 'host', 'port', 'protocol')
        ]