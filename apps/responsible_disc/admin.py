from django.contrib import admin
from apps.responsible_disc import models


admin.site.register(models.Vulnerability)
admin.site.register(models.VulnerabilityLog)
