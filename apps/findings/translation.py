from modeltranslation.translator import TranslationOptions, register
from apps.findings import models


@register(models.Template)
class TemplateTranslationOptions(TranslationOptions):
    fields = ["name", "description", "recommendation"]


@register(models.VulnerabilityCategory)
class CategoryTranslationOptions(TranslationOptions):
    fields = ["display_name"]
