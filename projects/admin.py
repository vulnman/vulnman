from django.contrib import admin
from projects import models

admin.site.register(models.Project)
admin.site.register(models.ProjectMember)
admin.site.register(models.Report)
admin.site.register(models.ProjectContact)