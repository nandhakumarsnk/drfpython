from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

