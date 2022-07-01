from django.contrib import admin
from apps.reporting import models


admin.site.register(models.Report)
admin.site.register(models.ReportRelease)
