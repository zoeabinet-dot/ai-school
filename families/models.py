from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()


class Family(models.Model):
    """
    Family model for managing family information and relationships
    """
    class FamilyStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        PENDING = 'pending', 'Pending'
        SUSPENDED = 'suspended', 'Suspended'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='family_profile')
    family_name = models.CharField(max_length=100, help_text="Family name or surname")
    primary_contact_name = models.CharField(max_length=100, help_text="Primary contact person's name")
    primary_contact_email = models.EmailField(help_text="Primary contact email address")
    primary_contact_phone = models.CharField(max_length=20, help_text="Primary contact phone number")
    address = models.TextField(help_text="Family address")
    location = models.CharField(max_length=100, help_text="City/region location")
    emergency_contact = models.JSONField(default=dict, help_text="Emergency contact information")
    status = models.CharField(max_length=20, choices=FamilyStatus.choices, default=FamilyStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Family'
        verbose_name_plural = 'Families'
        ordering = ['family_name']
    
    def __str__(self):
        return f"{self.family_name} Family"
    
    @property
    def total_members(self):
        return self.family_members.count()
    
    @property
    def total_students(self):
        return self.family_students.count()


class FamilyMember(models.Model):
    """
    Family member model for managing individual family members
    """
    class Relationship(models.TextChoices):
        PARENT = 'parent', 'Parent'
        GUARDIAN = 'guardian', 'Guardian'
        SIBLING = 'sibling', 'Sibling'
        GRANDPARENT = 'grandparent', 'Grandparent'
        UNCLE_AUNT = 'uncle_aunt', 'Uncle/Aunt'
        OTHER = 'other', 'Other'
    
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='family_members')
    name = models.CharField(max_length=100, help_text="Full name of family member")
    relationship = models.CharField(max_length=20, choices=Relationship.choices, help_text="Relationship to primary contact")
    date_of_birth = models.DateField(null=True, blank=True, help_text="Date of birth")
    contact_info = models.JSONField(default=dict, help_text="Contact information for this member")
    emergency_contact = models.BooleanField(default=False, help_text="Is this person an emergency contact?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Family Member'
        verbose_name_plural = 'Family Members'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_relationship_display()}) - {self.family.family_name}"
    
    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None


class FamilyStudent(models.Model):
    """
    Family-student relationship model for managing student-family connections
    """
    class GuardianStatus(models.TextChoices):
        PRIMARY = 'primary', 'Primary Guardian'
        SECONDARY = 'secondary', 'Secondary Guardian'
        EMERGENCY = 'emergency', 'Emergency Contact'
        OTHER = 'other', 'Other'
    
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='family_students')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='family_relationships')
    relationship = models.CharField(max_length=20, choices=FamilyMember.Relationship.choices, help_text="Relationship to student")
    guardian_status = models.CharField(max_length=20, choices=GuardianStatus.choices, default=GuardianStatus.PRIMARY)
    contact_preferences = models.JSONField(default=dict, help_text="Preferred contact methods and times")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Family Student'
        verbose_name_plural = 'Family Students'
        unique_together = ['family', 'student']
        ordering = ['family', 'student']
    
    def __str__(self):
        return f"{self.family.family_name} - {self.student.user.get_full_name()}"
    
    @property
    def is_primary_guardian(self):
        return self.guardian_status == self.GuardianStatus.PRIMARY


class FamilyCommunication(models.Model):
    """
    Family communication log for tracking interactions
    """
    class CommunicationType(models.TextChoices):
        EMAIL = 'email', 'Email'
        PHONE = 'phone', 'Phone'
        SMS = 'sms', 'SMS'
        IN_PERSON = 'in_person', 'In Person'
        VIDEO_CALL = 'video_call', 'Video Call'
        OTHER = 'other', 'Other'
    
    class CommunicationDirection(models.TextChoices):
        INBOUND = 'inbound', 'Inbound'
        OUTBOUND = 'outbound', 'Outbound'
    
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='communications')
    communication_type = models.CharField(max_length=20, choices=CommunicationType.choices)
    direction = models.CharField(max_length=20, choices=CommunicationDirection.choices)
    subject = models.CharField(max_length=200, blank=True, help_text="Communication subject")
    content = models.TextField(help_text="Communication content or summary")
    initiated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='initiated_communications')
    timestamp = models.DateTimeField(default=timezone.now)
    follow_up_required = models.BooleanField(default=False, help_text="Does this communication require follow-up?")
    follow_up_notes = models.TextField(blank=True, help_text="Notes for follow-up actions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Family Communication'
        verbose_name_plural = 'Family Communications'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.family.family_name} - {self.get_communication_type_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class FamilyNotification(models.Model):
    """
    Family notification preferences and settings
    """
    class NotificationType(models.TextChoices):
        ACADEMIC_PROGRESS = 'academic_progress', 'Academic Progress'
        BEHAVIOR_ALERTS = 'behavior_alerts', 'Behavior Alerts'
        ATTENDANCE = 'attendance', 'Attendance'
        GENERAL_ANNOUNCEMENTS = 'general_announcements', 'General Announcements'
        EMERGENCY = 'emergency', 'Emergency Notifications'
        OTHER = 'other', 'Other'
    
    class NotificationMethod(models.TextChoices):
        EMAIL = 'email', 'Email'
        SMS = 'sms', 'SMS'
        PUSH_NOTIFICATION = 'push_notification', 'Push Notification'
        IN_APP = 'in_app', 'In-App Notification'
    
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices)
    notification_method = models.CharField(max_length=20, choices=NotificationMethod.choices)
    enabled = models.BooleanField(default=True, help_text="Is this notification type enabled?")
    frequency = models.CharField(max_length=20, default='immediate', help_text="Notification frequency")
    custom_settings = models.JSONField(default=dict, help_text="Custom notification settings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Family Notification'
        verbose_name_plural = 'Family Notifications'
        unique_together = ['family', 'notification_type', 'notification_method']
        ordering = ['family', 'notification_type']
    
    def __str__(self):
        return f"{self.family.family_name} - {self.get_notification_type_display()} - {self.get_notification_method_display()}"
