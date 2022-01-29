from django.contrib import admin
from apps.findings import models


class TextProofInline(admin.StackedInline):
    model = models.TextProof
    exclude = ["project", "command_created"]


class ImageProofInline(admin.StackedInline):
    model = models.ImageProof
    exclude = ["project", "command_created"]


class TemplateReferenceInline(admin.StackedInline):
    model = models.Reference
    exclude = ["vulnerability"]


class VulnerabilityAdmin(admin.ModelAdmin):
    inlines = [TextProofInline, ImageProofInline]
    exclude = ["command_created"]


class TemplateAdmin(admin.ModelAdmin):
    inlines = [TemplateReferenceInline]


admin.site.register(models.Vulnerability, VulnerabilityAdmin)
admin.site.register(models.Template, TemplateAdmin)
admin.site.register(models.Finding)
