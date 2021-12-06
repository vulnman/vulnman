from django.contrib import admin
from apps.social import models


admin.site.register(models.Employee)
admin.site.register(models.Credential)
