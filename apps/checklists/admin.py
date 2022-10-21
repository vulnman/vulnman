from django.contrib import admin
from . import models


class ConditionInline(admin.StackedInline):
    model = models.Condition


class TaskAdmin(admin.ModelAdmin):
    inlines = [ConditionInline]


admin.site.register(models.ChecklistTask, TaskAdmin)
admin.site.register(models.ProjectTask)
