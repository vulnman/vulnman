from django.contrib import admin
from core import models


admin.site.register(models.AssetTask)
admin.site.register(models.Task)
admin.site.register(models.TaskCondition)
