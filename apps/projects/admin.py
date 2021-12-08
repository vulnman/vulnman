from django.contrib import admin
from apps.projects import models

admin.site.register(models.Project)
admin.site.register(models.ProjectMember)
admin.site.register(models.ProjectContact)
admin.site.register(models.CommandHistoryItem)
