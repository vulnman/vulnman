from django.contrib import admin
from apps.reporting import models


class ReportShareTokenInline(admin.StackedInline):
    model = models.ReportShareToken
    readonly_fields = ["share_token"]


class ReportAdmin(admin.ModelAdmin):
    inlines = [ReportShareTokenInline]


# Register your models here.
admin.site.register(models.PentestReport)
admin.site.register(models.ReportInformation)
