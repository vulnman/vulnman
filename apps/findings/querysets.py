from django.db.models import QuerySet, Manager
from django.contrib.contenttypes.models import ContentType
from apps.assets import models as asset_models


class VulnerabilityQuerySet(QuerySet):
    def open(self):
        return self.filter(status=self.model.STATUS_OPEN)

    def fixed(self):
        return self.filter(status=self.model.STATUS_FIXED)

    def for_project(self, project):
        return self.filter(project=project)


class VulnerabilityManager(Manager):
    def get_asset_content_type(self, asset_pk):
        model_classes = [asset_models.Host, asset_models.WebApplication,
                         asset_models.WebRequest, asset_models.Service]
        for model_class in model_classes:
            qs = model_class.objects.filter(pk=asset_pk)
            if qs.exists():
                return ContentType.objects.get_for_model(model_class)
        raise Exception("Invalid Asset Type")
