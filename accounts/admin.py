from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("User management", {"fields": ("is_manager", "created_by")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("User management", {"fields": ("is_manager", "created_by")}),
    )
    list_display = UserAdmin.list_display + ("is_manager", "created_by")
    list_filter = UserAdmin.list_filter + ("is_manager",)
