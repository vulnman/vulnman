from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account import models


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'user_role')}
         ),
    )


admin.site.register(models.User, CustomUserAdmin)
