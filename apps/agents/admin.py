from django.contrib import admin
from apps.agents import models


# Register your models here.
admin.site.register(models.Agent)
admin.site.register(models.AgentQueue)
