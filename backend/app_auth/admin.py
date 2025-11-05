from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_admin', 'is_active', 'created_at')
    list_filter = ('is_admin', 'is_active', 'created_at')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_admin'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ()  
