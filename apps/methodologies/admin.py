from django.contrib import admin
from apps.methodologies import models

# Register your models here.
admin.site.register(models.Task)
admin.site.register(models.TaskCondition)
admin.site.register(models.AssetTask)
