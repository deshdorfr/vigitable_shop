from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("id",)
    list_display = ("id", "mobile", "name", "email", "is_staff", "is_active")
    search_fields = ("mobile", "name", "email")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        ("Login", {"fields": ("mobile", "password")}),
        ("Profile", {"fields": ("name", "email")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("mobile", "name", "email", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    inlines = [AddressInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "mobile", "city", "state", "pincode", "is_default")
    search_fields = ("full_name", "mobile", "city", "state", "pincode", "user__mobile")
    list_filter = ("city", "state", "is_default")
