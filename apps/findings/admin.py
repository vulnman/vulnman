from django.contrib import admin
from apps.findings import models


class VulnerabilityDetailsInline(admin.StackedInline):
    model = models.VulnerabilityDetails
    exclude = ["template"]


class VulnerabilityReferenceInline(admin.StackedInline):
    model = models.Reference
    exclude = ["template"]


class VulnerabilityProofsInline(admin.StackedInline):
    model = models.ProofOfConcept
    exclude = ["template"]


class TemplateReferenceInline(admin.StackedInline):
    model = models.Reference
    exclude = ["vulnerability"]


class TemplateDetailsInline(admin.StackedInline):
    model = models.VulnerabilityDetails
    exclude = ["vulnerability"]


class VulnerabilityAdmin(admin.ModelAdmin):
    inlines = [VulnerabilityDetailsInline, VulnerabilityReferenceInline, VulnerabilityProofsInline]


class TemplateAdmin(admin.ModelAdmin):
    inlines = [TemplateDetailsInline, TemplateReferenceInline]


admin.site.register(models.Vulnerability, VulnerabilityAdmin)
admin.site.register(models.Template, TemplateAdmin)
admin.site.register(models.Finding)
