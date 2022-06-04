from django.contrib import admin
from apps.projects import models


class ClientContactInline(admin.StackedInline):
    model = models.ClientContact


class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientContactInline]


admin.site.register(models.Project)
admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.ProjectContributor)
