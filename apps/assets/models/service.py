from django.db import models
from django.urls import reverse_lazy
from apps.assets.models.base import BaseAsset


class Service(BaseAsset):
    ASSET_TYPE = "service"
    ASSET_TYPE_CHOICE = (ASSET_TYPE, "Service")

    STATE_CLOSED = "closed"
    STATE_OPEN = "open"
    STATE_FILTERED = "filtered"
    PROTOCOL_TCP = "tcp"
    PROTOCOL_UDP = "udp"

    STATE_CHOICES = [
        (STATE_CLOSED, "Closed"),
        (STATE_OPEN, "Open"),
        (STATE_FILTERED, "Filtered")
    ]
    PROTOCOL_CHOICES = [
        (PROTOCOL_TCP, "TCP"),
        (PROTOCOL_UDP, "UDP")
    ]

    port = models.PositiveIntegerField(blank=True, null=True)
    host = models.ForeignKey('assets.Host', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=True)
    protocol = models.CharField(
        max_length=12, default=PROTOCOL_TCP, choices=PROTOCOL_CHOICES)
    state = models.CharField(
        max_length=24, default=STATE_FILTERED, choices=STATE_CHOICES)
    banner = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = [
            ('project', 'host', 'port', 'protocol')
        ]

    def __str__(self):
        return "%s/%s %s (%s)" % (
            self.protocol, self.port, self.name, self.host.ip)

    def get_absolute_url(self):
        return reverse_lazy(
            "projects:assets:service-detail", kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy(
            "projects:assets:service-delete", kwargs={"pk": self.pk})
