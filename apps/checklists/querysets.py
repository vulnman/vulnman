from django.db.models import QuerySet, Manager
from django.contrib.contenttypes.models import ContentType


class AssetTechnologyQuerySet(QuerySet):
    def for_asset(self, asset):
        ct = ContentType.objects.get_for_model(asset._meta.model)
        return self.filter(content_type=ct, object_id=asset.pk)

    def for_project(self, project):
        return self.filter(project=project)


class AssetTechnologyManager(Manager):
    pass
