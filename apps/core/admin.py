"""
Admin configuration for core models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Role, RoleTag, UserRole, UserRoleTag


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'dashboard_url', 'display_order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['display_order', 'name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'description')
        }),
        ('Dashboard', {
            'fields': ('dashboard_url', 'dashboard_icon', 'display_order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RoleTag)
class RoleTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'applicable_to_role', 'is_active']
    list_filter = ['is_active', 'applicable_to_role', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['applicable_to_role']

    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'description', 'applicable_to_role')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class UserRoleInline(admin.TabularInline):
    model = UserRole
    fk_name = 'user'
    extra = 1
    autocomplete_fields = ['role']
    readonly_fields = ['assigned_at']


class UserRoleTagInline(admin.TabularInline):
    model = UserRoleTag
    fk_name = 'user'
    extra = 1
    autocomplete_fields = ['role_tag']
    readonly_fields = ['assigned_at']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'get_full_name', 'get_roles_display', 'email_status', 'active_status', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'email_confirmed', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined', 'last_login', 'created_at', 'updated_at']

    fieldsets = (
        ('Login Credentials', {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'email_confirmed')
        }),
        ('Important dates', {
            'fields': ('date_joined', 'last_login', 'created_at', 'updated_at', 'deleted_at')
        }),
    )

    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'email_confirmed'),
        }),
    )

    inlines = [UserRoleInline, UserRoleTagInline]

    def email_status(self, obj):
        if obj.email_confirmed:
            return format_html('<span style="color: green;">✓ Confirmed</span>')
        return format_html('<span style="color: red;">✗ Not Confirmed</span>')
    email_status.short_description = 'Email Status'

    def active_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: orange;">✗ Inactive</span>')
    active_status.short_description = 'Active Status'

    def get_roles_display(self, obj):
        roles = obj.roles.all()
        if roles:
            return ', '.join([role.name for role in roles])
        return '-'
    get_roles_display.short_description = 'Roles'


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'assigned_at', 'assigned_by']
    list_filter = ['role', 'assigned_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    autocomplete_fields = ['user', 'role', 'assigned_by']
    readonly_fields = ['assigned_at']


@admin.register(UserRoleTag)
class UserRoleTagAdmin(admin.ModelAdmin):
    list_display = ['user', 'role_tag', 'assigned_at', 'assigned_by']
    list_filter = ['role_tag', 'assigned_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    autocomplete_fields = ['user', 'role_tag', 'assigned_by']
    readonly_fields = ['assigned_at']
