from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    """
    Student model extending the User model with academic information
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    
    # Academic information
    student_id = models.CharField(max_length=20, unique=True, help_text="Unique student identifier")
    grade_level = models.CharField(max_length=20, choices=[
        ('K', 'Kindergarten'),
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
    ])
    academic_year = models.CharField(max_length=20)
    enrollment_date = models.DateField()
    
    # Academic status
    is_active_student = models.BooleanField(default=True)
    academic_status = models.CharField(max_length=20, choices=[
        ('enrolled', 'Enrolled'),
        ('graduated', 'Graduated'),
        ('transferred', 'Transferred'),
        ('suspended', 'Suspended'),
        ('withdrawn', 'Withdrawn'),
    ], default='enrolled')
    
    # Learning preferences
    learning_style = models.CharField(max_length=50, choices=[
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('kinesthetic', 'Kinesthetic'),
        ('reading', 'Reading/Writing'),
        ('mixed', 'Mixed'),
    ], blank=True, null=True)
    
    preferred_language = models.CharField(max_length=10, default='en')
    
    # AI Learning settings
    ai_learning_enabled = models.BooleanField(default=True)
    ai_difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='intermediate')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'students'
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Grade {self.grade_level}"


class AcademicRecord(models.Model):
    """
    Academic performance and progress tracking
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='academic_records')
    
    # Subject information
    subject = models.CharField(max_length=100)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=20)
    
    # Performance metrics
    grade = models.CharField(max_length=5, choices=[
        ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
        ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
        ('D+', 'D+'), ('D', 'D'), ('D-', 'D-'),
        ('F', 'F'), ('P', 'Pass'), ('I', 'Incomplete'),
    ])
    
    score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Additional metrics
    attendance_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    participation_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    # AI-generated insights
    ai_recommendations = models.JSONField(default=dict, blank=True)
    learning_gaps = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'academic_records'
        unique_together = ['student', 'subject', 'semester', 'academic_year']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject} ({self.semester})"


class StudentProject(models.Model):
    """
    Student portfolio projects and creative work
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='projects')
    
    # Project information
    title = models.CharField(max_length=200)
    description = models.TextField()
    project_type = models.CharField(max_length=50, choices=[
        ('art', 'Art'),
        ('code', 'Code/Programming'),
        ('video', 'Video'),
        ('writing', 'Writing'),
        ('science', 'Science'),
        ('math', 'Mathematics'),
        ('social_studies', 'Social Studies'),
        ('other', 'Other'),
    ])
    
    # Project files
    project_file = models.FileField(upload_to='student_projects/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='project_thumbnails/', blank=True, null=True)
    
    # Project metadata
    tags = models.JSONField(default=list, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ])
    
    # AI assessment
    ai_feedback = models.TextField(blank=True, null=True)
    ai_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    # Project status
    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_projects'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.student.user.get_full_name()}"


class LearningSession(models.Model):
    """
    Track individual learning sessions and engagement
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='learning_sessions')
    
    # Session information
    session_type = models.CharField(max_length=50, choices=[
        ('ai_lesson', 'AI Lesson'),
        ('video_lesson', 'Video Lesson'),
        ('quiz', 'Quiz'),
        ('project_work', 'Project Work'),
        ('reading', 'Reading'),
        ('practice', 'Practice Exercise'),
    ])
    
    # Duration and engagement
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    
    # Engagement metrics
    attention_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    engagement_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], blank=True, null=True)
    
    # AI monitoring data
    webcam_analysis = models.JSONField(default=dict, blank=True)
    behavior_notes = models.TextField(blank=True, null=True)
    
    # Learning outcomes
    completed = models.BooleanField(default=False)
    performance_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    # Session metadata
    lesson_id = models.CharField(max_length=100, blank=True, null=True)
    device_info = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'learning_sessions'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.session_type} at {self.start_time}"
    
    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds() / 60
            self.duration_minutes = round(duration, 2)
        super().save(*args, **kwargs)


class StudentGoal(models.Model):
    """
    Student learning goals and objectives
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='goals')
    
    # Goal information
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_type = models.CharField(max_length=50, choices=[
        ('academic', 'Academic'),
        ('skill', 'Skill Development'),
        ('behavioral', 'Behavioral'),
        ('social', 'Social'),
        ('personal', 'Personal'),
    ])
    
    # Goal parameters
    target_date = models.DateField()
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='medium')
    
    # Progress tracking
    progress_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    
    status = models.CharField(max_length=20, choices=[
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ], default='not_started')
    
    # AI assistance
    ai_suggestions = models.JSONField(default=list, blank=True)
    ai_milestones = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_goals'
        ordering = ['-priority', 'target_date']
    
    def __str__(self):
        return f"{self.title} - {self.student.user.get_full_name()}"
