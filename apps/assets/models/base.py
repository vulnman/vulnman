from django.db import models
from vulnman.models import VulnmanProjectModel
from django.contrib.contenttypes.fields import GenericRelation


class BaseAsset(VulnmanProjectModel):
    description = models.TextField(blank=True)
    hide_from_report = models.BooleanField(default=False)
    vulnerability_relation = GenericRelation("findings.Vulnerability", content_type_field="content_type",
                                             object_id_field="object_id")

    class Meta:
        abstract = True

    @property
    def asset_type(self):
        return self._meta.verbose_name
