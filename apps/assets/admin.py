from django.contrib import admin
from apps.assets import models

admin.site.register(models.WebApplication)
admin.site.register(models.WebRequest)
admin.site.register(models.Host)
admin.site.register(models.Service)