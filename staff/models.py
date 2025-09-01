from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()


class Staff(models.Model):
    """
    Staff model for managing staff members and their roles
    """
    class Department(models.TextChoices):
        TEACHING = 'teaching', 'Teaching'
        ADMINISTRATION = 'administration', 'Administration'
        SUPPORT = 'support', 'Support'
        TECHNOLOGY = 'technology', 'Technology'
        HEALTH = 'health', 'Health Services'
        SECURITY = 'security', 'Security'
        MAINTENANCE = 'maintenance', 'Maintenance'
        OTHER = 'other', 'Other'
    
    class StaffRole(models.TextChoices):
        TEACHER = 'teacher', 'Teacher'
        TEACHING_ASSISTANT = 'teaching_assistant', 'Teaching Assistant'
        ADMINISTRATOR = 'administrator', 'Administrator'
        COUNSELOR = 'counselor', 'Counselor'
        LIBRARIAN = 'librarian', 'Librarian'
        NURSE = 'nurse', 'Nurse'
        TECHNICIAN = 'technician', 'Technician'
        COORDINATOR = 'coordinator', 'Coordinator'
        OTHER = 'other', 'Other'
    
    class StaffStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        ON_LEAVE = 'on_leave', 'On Leave'
        TERMINATED = 'terminated', 'Terminated'
        PROBATION = 'probation', 'Probation'
        
    class GradeLevels(models.TextChoices):
        PRE_K = 'pre_k', 'Pre-K'
        KINDERGARTEN = 'k', 'Kindergarten'
        FIRST = '1', 'First Grade'
        SECOND = '2', 'Second Grade'
        THIRD = '3', 'Third Grade'
        FOURTH = '4', 'Fourth Grade'
        FIFTH = '5', 'Fifth Grade'
        SIXTH = '6', 'Sixth Grade'
        SEVENTH = '7', 'Seventh Grade'
        EIGHTH = '8', 'Eighth Grade'
        NINTH = '9', 'Ninth Grade'
        TENTH = '10', 'Tenth Grade'
        ELEVENTH = '11', 'Eleventh Grade'
        TWELFTH = '12', 'Twelfth Grade'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=20, unique=True, help_text="Unique employee ID")
    department = models.CharField(max_length=20, choices=Department.choices, help_text="Staff department")
    role = models.CharField(max_length=20, choices=StaffRole.choices, help_text="Staff role")
    hire_date = models.DateField(help_text="Date of hire")
    status = models.CharField(max_length=20, choices=StaffStatus.choices, default=StaffStatus.ACTIVE)
    qualifications = models.JSONField(default=list, help_text="List of qualifications and certifications")
    specializations = models.JSONField(default=list, help_text="Areas of specialization")
    assigned_grades = models.JSONField(default=list, help_text="Grade levels assigned to this staff member")
    assigned_subjects = models.JSONField(default=list, help_text="Subjects assigned to this staff member")
    teaching_experience = models.PositiveIntegerField(default=0, help_text="Years of teaching experience")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff Members'
        ordering = ['employee_id']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()} ({self.employee_id})"
    
    @property
    def years_of_service(self):
        today = timezone.now().date()
        return today.year - self.hire_date.year - ((today.month, today.day) < (self.hire_date.month, self.hire_date.day))


class StaffProfile(models.Model):
    """
    Extended staff profile information
    """
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='profile')
    certifications = models.JSONField(default=list, help_text="Professional certifications")
    preferences = models.JSONField(default=dict, help_text="Staff preferences and settings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Staff Profile'
        verbose_name_plural = 'Staff Profiles'
    
    def __str__(self):
        return f"Profile for {self.staff.user.get_full_name()}"


class StaffAssignment(models.Model):
    """
    Staff assignment model for managing staff responsibilities
    """
    class AssignmentType(models.TextChoices):
        TEACHING = 'teaching', 'Teaching'
        SUPERVISION = 'supervision', 'Supervision'
        ADMINISTRATIVE = 'administrative', 'Administrative'
        SUPPORT = 'support', 'Support'
        SPECIAL_PROJECT = 'special_project', 'Special Project'
        OTHER = 'other', 'Other'
    
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='assignments')
    assignment_type = models.CharField(max_length=20, choices=AssignmentType.choices)
    title = models.CharField(max_length=200, help_text="Assignment title")
    description = models.TextField(help_text="Assignment description")
    start_date = models.DateField(help_text="Assignment start date")
    end_date = models.DateField(null=True, blank=True, help_text="Assignment end date (if applicable)")
    is_active = models.BooleanField(default=True, help_text="Is this assignment currently active?")
    responsibilities = models.JSONField(default=list, help_text="List of responsibilities")
    performance_metrics = models.JSONField(default=dict, help_text="Performance evaluation metrics")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Staff Assignment'
        verbose_name_plural = 'Staff Assignments'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.staff.user.get_full_name()} - {self.title}"
    
    @property
    def duration_days(self):
        if self.end_date:
            return (self.end_date - self.start_date).days
        return (timezone.now().date() - self.start_date).days


class StaffSchedule(models.Model):
    """
    Staff schedule model for managing work schedules
    """
    class DayOfWeek(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'
    
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    start_time = models.TimeField(help_text="Start time for this day")
    end_time = models.TimeField(help_text="End time for this day")
    is_working_day = models.BooleanField(default=True, help_text="Is this a working day?")
    break_start = models.TimeField(null=True, blank=True, help_text="Break start time")
    break_end = models.TimeField(null=True, blank=True, help_text="Break end time")
    notes = models.TextField(blank=True, help_text="Additional notes for this schedule")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Staff Schedule'
        verbose_name_plural = 'Staff Schedules'
        unique_together = ['staff', 'day_of_week']
        ordering = ['staff', 'day_of_week']
    
    def __str__(self):
        return f"{self.staff.user.get_full_name()} - {self.get_day_of_week_display()} ({self.start_time} - {self.end_time})"


class StaffPerformance(models.Model):
    """
    Staff performance evaluation model
    """
    class PerformanceRating(models.TextChoices):
        EXCELLENT = 'excellent', 'Excellent'
        GOOD = 'good', 'Good'
        SATISFACTORY = 'satisfactory', 'Satisfactory'
        NEEDS_IMPROVEMENT = 'needs_improvement', 'Needs Improvement'
        UNSATISFACTORY = 'unsatisfactory', 'Unsatisfactory'
    
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='performance_records')
    evaluation_period = models.CharField(max_length=50, help_text="Evaluation period (e.g., 'Q1 2024')")
    evaluation_date = models.DateField(default=timezone.now, help_text="Date of evaluation")
    overall_rating = models.CharField(max_length=20, choices=PerformanceRating.choices)
    strengths = models.JSONField(default=list, help_text="List of strengths")
    areas_for_improvement = models.JSONField(default=list, help_text="Areas that need improvement")
    goals = models.JSONField(default=list, help_text="Performance goals for next period")
    evaluator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluations_given')
    comments = models.TextField(blank=True, help_text="Additional comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Staff Performance'
        verbose_name_plural = 'Staff Performance Records'
        ordering = ['-evaluation_date']
    
    def __str__(self):
        return f"{self.staff.user.get_full_name()} - {self.evaluation_period} ({self.get_overall_rating_display()})"
