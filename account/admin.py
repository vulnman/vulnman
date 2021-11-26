from django.contrib import admin
from django.contrib.auth.models import User
from account import models


class ProfileInline(admin.StackedInline):
    model = models.Profile


class ExtendedUserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
