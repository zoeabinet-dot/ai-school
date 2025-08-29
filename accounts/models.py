from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom User model with role-based access"""
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('family', 'Family/Guardian'),
        ('staff', 'Staff/Teacher Assistant'),
        ('admin', 'Administrator'),
        ('ai_teacher', 'AI Teacher'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Student(models.Model):
    """Student profile extending User"""
    
    GRADE_CHOICES = [
        ('kg', 'Kindergarten'),
        ('1', 'Grade 1'),
        ('2', 'Grade 2'),
        ('3', 'Grade 3'),
        ('4', 'Grade 4'),
        ('5', 'Grade 5'),
        ('6', 'Grade 6'),
        ('7', 'Grade 7'),
        ('8', 'Grade 8'),
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    grade_level = models.CharField(max_length=5, choices=GRADE_CHOICES)
    enrollment_date = models.DateField(default=timezone.now)
    learning_preferences = models.JSONField(default=dict, blank=True)
    special_needs = models.TextField(blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # AI Learning Metrics
    learning_pace = models.CharField(max_length=20, default='medium')  # slow, medium, fast
    preferred_learning_style = models.CharField(max_length=20, default='visual')  # visual, auditory, kinesthetic
    attention_span_minutes = models.IntegerField(default=30)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"


class Family(models.Model):
    """Family/Guardian profile extending User"""
    
    RELATIONSHIP_CHOICES = [
        ('parent', 'Parent'),
        ('guardian', 'Guardian'),
        ('grandparent', 'Grandparent'),
        ('sibling', 'Sibling'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='family_profile')
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    students = models.ManyToManyField(Student, related_name='families')
    occupation = models.CharField(max_length=100, blank=True, null=True)
    workplace = models.CharField(max_length=100, blank=True, null=True)
    preferred_communication = models.CharField(max_length=20, default='email')  # email, phone, sms
    notification_preferences = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_relationship_display()})"


class Staff(models.Model):
    """Staff/Teacher Assistant profile extending User"""
    
    POSITION_CHOICES = [
        ('teacher_assistant', 'Teacher Assistant'),
        ('counselor', 'Counselor'),
        ('coordinator', 'Learning Coordinator'),
        ('supervisor', 'Supervisor'),
        ('support_staff', 'Support Staff'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    position = models.CharField(max_length=30, choices=POSITION_CHOICES)
    department = models.CharField(max_length=50, blank=True, null=True)
    hire_date = models.DateField(default=timezone.now)
    qualifications = models.TextField(blank=True, null=True)
    specializations = models.JSONField(default=list, blank=True)
    assigned_students = models.ManyToManyField(Student, related_name='assigned_staff', blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_position_display()}"


class Administrator(models.Model):
    """Administrator profile extending User"""
    
    ACCESS_LEVEL_CHOICES = [
        ('basic', 'Basic Admin'),
        ('advanced', 'Advanced Admin'),
        ('super', 'Super Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES)
    permissions = models.JSONField(default=dict, blank=True)
    managed_departments = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_access_level_display()}"


class UserSession(models.Model):
    """Track user sessions for analytics"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_start = models.DateTimeField(auto_now_add=True)
    session_end = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_type = models.CharField(max_length=20, default='unknown')  # mobile, tablet, desktop
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.session_start}"
    
    @property
    def duration(self):
        if self.session_end:
            return self.session_end - self.session_start
        return timezone.now() - self.session_start


class UserPreferences(models.Model):
    """User preferences and settings"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    theme = models.CharField(max_length=20, default='light')  # light, dark
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='Africa/Addis_Ababa')
    notification_settings = models.JSONField(default=dict, blank=True)
    dashboard_layout = models.JSONField(default=dict, blank=True)
    accessibility_settings = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.user.username} preferences"