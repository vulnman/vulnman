from django.contrib import admin
from apps.reporting import models


admin.site.register(models.PentestReport)
admin.site.register(models.ReportInformation)
