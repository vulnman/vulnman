from django.contrib import admin
from apps.commands import models


admin.site.register(models.CommandTemplate)
admin.site.register(models.CommandHistoryItem)
