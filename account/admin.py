from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from account import models


class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False
    max_num = 1


class ExtendedUserAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
