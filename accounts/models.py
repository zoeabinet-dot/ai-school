from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model supporting multiple roles in the AI School Management System
    """
    
    class UserRole(models.TextChoices):
        STUDENT = 'student', _('Student')
        FAMILY = 'family', _('Family/Guardian')
        STAFF = 'staff', _('Staff/Teacher Assistant')
        ADMIN = 'admin', _('Administrator')
        AI_TEACHER = 'ai_teacher', _('AI Teacher')
    
    # Basic profile fields
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT
    )
    
    # Personal information
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    
    # Address information
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='Ethiopia')
    
    # Additional fields
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    @property
    def is_student(self):
        return self.role == self.UserRole.STUDENT
    
    @property
    def is_family(self):
        return self.role == self.UserRole.FAMILY
    
    @property
    def is_staff_member(self):
        return self.role == self.UserRole.STAFF
    
    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN
    
    @property
    def is_ai_teacher(self):
        return self.role == self.UserRole.AI_TEACHER


class UserProfile(models.Model):
    """
    Extended profile information for users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Academic information (for students)
    grade_level = models.CharField(max_length=20, blank=True, null=True)
    academic_year = models.CharField(max_length=20, blank=True, null=True)
    
    # Family information (for family members)
    relationship_to_student = models.CharField(max_length=50, blank=True, null=True)
    
    # Staff information
    department = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    
    # Preferences
    language_preference = models.CharField(max_length=10, default='en')
    notification_preferences = models.JSONField(default=dict)
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"Profile for {self.user.username}"


class UserSession(models.Model):
    """
    Track user sessions for analytics and security
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_sessions'
    
    def __str__(self):
        return f"Session for {self.user.username} at {self.login_time}"


class Permission(models.Model):
    """
    Custom permissions for role-based access control
    """
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'permissions'
    
    def __str__(self):
        return self.name


class RolePermission(models.Model):
    """
    Many-to-many relationship between roles and permissions
    """
    role = models.CharField(max_length=20, choices=User.UserRole.choices)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'role_permissions'
        unique_together = ['role', 'permission']
    
    def __str__(self):
        return f"{self.role} - {self.permission.name}"
