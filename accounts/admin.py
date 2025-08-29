from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, UserSession, Permission, RolePermission


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email', 'phone_number', 
                'date_of_birth', 'profile_picture', 'bio'
            )
        }),
        (_('Location'), {'fields': ('address', 'city', 'country')}),
        (_('Role & Permissions'), {
            'fields': (
                'role', 'is_active', 'is_staff', 'is_superuser', 
                'groups', 'user_permissions'
            )
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Email Verification'), {'fields': ('email_verified', 'email_verification_token')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'role',
                'first_name', 'last_name'
            ),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade_level', 'department', 'position', 'created_at')
    list_filter = ('grade_level', 'department', 'position', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Academic Information'), {'fields': ('grade_level', 'academic_year')}),
        (_('Family Information'), {'fields': ('relationship_to_student',)}),
        (_('Staff Information'), {'fields': ('department', 'position', 'hire_date')}),
        (_('Preferences'), {'fields': ('language_preference', 'notification_preferences')}),
        (_('Emergency Contact'), {
            'fields': (
                'emergency_contact_name', 'emergency_contact_phone', 
                'emergency_contact_relationship'
            )
        }),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'login_time', 'logout_time', 'is_active')
    list_filter = ('is_active', 'login_time', 'logout_time')
    search_fields = ('user__username', 'user__email', 'ip_address')
    ordering = ('-login_time',)
    
    fieldsets = (
        (_('Session Info'), {'fields': ('user', 'session_key', 'is_active')}),
        (_('Connection Details'), {'fields': ('ip_address', 'user_agent')}),
        (_('Timestamps'), {'fields': ('login_time', 'logout_time')}),
    )
    
    readonly_fields = ('login_time', 'logout_time')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'description')
    search_fields = ('name', 'codename', 'description')
    ordering = ('name',)
    
    fieldsets = (
        (None, {'fields': ('name', 'codename', 'description')}),
    )


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')
    list_filter = ('role',)
    search_fields = ('role', 'permission__name')
    ordering = ('role', 'permission__name')
    
    fieldsets = (
        (None, {'fields': ('role', 'permission')}),
    )
