from django.contrib import admin
from apps.methodologies import models

# Register your models here.
admin.site.register(models.Methodology)
admin.site.register(models.SuggestedCommand)
