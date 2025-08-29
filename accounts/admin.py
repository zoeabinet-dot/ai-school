from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Student, Family, Staff, Administrator, UserSession, UserPreferences


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'role', 
        'is_verified', 'is_active', 'created_at'
    ]
    list_filter = ['role', 'is_verified', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'role', 'phone_number', 'profile_picture', 'date_of_birth',
                'address', 'emergency_contact', 'emergency_phone', 'is_verified'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Student admin"""
    
    list_display = [
        'student_id', 'get_full_name', 'grade_level', 'enrollment_date',
        'learning_pace', 'is_active'
    ]
    list_filter = ['grade_level', 'learning_pace', 'is_active', 'enrollment_date']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    ordering = ['-enrollment_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'student_id', 'grade_level', 'enrollment_date')
        }),
        ('Learning Profile', {
            'fields': (
                'learning_preferences', 'learning_pace', 'preferred_learning_style',
                'attention_span_minutes'
            )
        }),
        ('Health & Special Needs', {
            'fields': ('special_needs', 'medical_conditions'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    """Family admin"""
    
    list_display = [
        'get_full_name', 'relationship', 'get_students_count',
        'preferred_communication', 'occupation'
    ]
    list_filter = ['relationship', 'preferred_communication']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'occupation']
    filter_horizontal = ['students']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'relationship')
        }),
        ('Professional Information', {
            'fields': ('occupation', 'workplace')
        }),
        ('Communication Preferences', {
            'fields': ('preferred_communication', 'notification_preferences')
        }),
        ('Students', {
            'fields': ('students',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def get_students_count(self, obj):
        return obj.students.count()
    get_students_count.short_description = 'Students Count'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('students')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """Staff admin"""
    
    list_display = [
        'employee_id', 'get_full_name', 'position', 'department',
        'hire_date', 'get_assigned_students_count', 'is_active'
    ]
    list_filter = ['position', 'department', 'is_active', 'hire_date']
    search_fields = [
        'employee_id', 'user__first_name', 'user__last_name', 
        'user__email', 'department'
    ]
    filter_horizontal = ['assigned_students']
    ordering = ['-hire_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'employee_id', 'position', 'department', 'hire_date')
        }),
        ('Qualifications', {
            'fields': ('qualifications', 'specializations'),
            'classes': ('collapse',)
        }),
        ('Assignments', {
            'fields': ('assigned_students',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def get_assigned_students_count(self, obj):
        return obj.assigned_students.count()
    get_assigned_students_count.short_description = 'Assigned Students'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('assigned_students')


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    """Administrator admin"""
    
    list_display = ['get_full_name', 'access_level', 'get_managed_departments']
    list_filter = ['access_level']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'access_level')
        }),
        ('Permissions & Access', {
            'fields': ('permissions', 'managed_departments')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def get_managed_departments(self, obj):
        return ', '.join(obj.managed_departments) if obj.managed_departments else 'None'
    get_managed_departments.short_description = 'Managed Departments'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """User Session admin"""
    
    list_display = [
        'user', 'session_start', 'session_end', 'get_duration',
        'device_type', 'is_active'
    ]
    list_filter = ['device_type', 'is_active', 'session_start']
    search_fields = ['user__username', 'user__email', 'ip_address']
    readonly_fields = ['session_start', 'get_duration']
    ordering = ['-session_start']
    
    def get_duration(self, obj):
        duration = obj.duration
        if duration:
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        return "Active"
    get_duration.short_description = 'Duration'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    """User Preferences admin"""
    
    list_display = ['user', 'theme', 'language', 'timezone']
    list_filter = ['theme', 'language', 'timezone']
    search_fields = ['user__username', 'user__email']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


# Customize admin site
admin.site.site_header = "School Management System"
admin.site.site_title = "SMS Admin"
admin.site.index_title = "Welcome to School Management System Administration"