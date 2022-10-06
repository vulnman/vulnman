from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from vulnman.models import VulnmanProjectModel, VulnmanModel
from apps.checklists import querysets


class Technology(VulnmanModel):
    name = models.CharField(max_length=128)
    programming_language = models.CharField(max_length=128, blank=True, null=True)
    homepage = models.URLField(blank=True, null=True)
    version = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date_updated"]
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        unique_together = [
            ('name', 'version')
        ]


class AssetTechnology(VulnmanProjectModel):
    ASSET_TYPES_CHOICES = [
        ("webapplication", "Web Application"),
        ("host", "Host"),
        ("service", "Service")
    ]
    objects = querysets.AssetTechnologyManager.from_queryset(querysets.AssetTechnologyQuerySet)()
    asset_type = models.CharField(max_length=64, choices=ASSET_TYPES_CHOICES, default="webapplication")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    asset = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["-date_updated"]
