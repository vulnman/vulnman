from django.contrib import admin
from apps.reporting import models


class ReportShareTokenInline(admin.StackedInline):
    model = models.ReportShareToken
    readonly_fields = ["share_token"]


class ReportSectionInline(admin.StackedInline):
    model = models.ReportSection
    exclude = ["command_created"]


class ReportAdmin(admin.ModelAdmin):
    inlines = [ReportSectionInline, ReportShareTokenInline]


# Register your models here.
admin.site.register(models.Report, ReportAdmin)
