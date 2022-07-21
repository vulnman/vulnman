from django.db.models import QuerySet, Manager
from django.contrib.contenttypes.models import ContentType
from apps.assets import models as asset_models


class TemplateQuerySet(QuerySet):
    def unique_and_ordered_for_project(self, project):
        template_pks = project.vulnerability_set.all().values_list("template__pk", flat=True)
        from collections import OrderedDict
        ordered = list(OrderedDict.fromkeys(template_pks))
        templates = []
        for template_pk in ordered:
            templates.append(self.get(pk=template_pk))
        return templates


class VulnerabilityQuerySet(QuerySet):
    def open(self):
        return self.filter(status=self.model.STATUS_OPEN)

    def fixed(self):
        return self.filter(status=self.model.STATUS_FIXED)

    def for_project(self, project):
        return self.filter(project=project)

    def with_asset(self, asset):
        ct = ContentType.objects.get_for_model(asset._meta.model)
        return self.filter(content_type=ct, object_id=asset.pk)

    def for_report(self, report_release):
        pass


class VulnerabilityManager(Manager):
    def get_asset_content_type(self, asset_pk):
        model_classes = [asset_models.Host, asset_models.WebApplication,
                         asset_models.WebRequest, asset_models.Service]
        for model_class in model_classes:
            qs = model_class.objects.filter(pk=asset_pk)
            if qs.exists():
                return ContentType.objects.get_for_model(model_class)
        raise Exception("Invalid Asset Type")
