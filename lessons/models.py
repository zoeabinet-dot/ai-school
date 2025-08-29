from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()


class Lesson(models.Model):
    """
    Lesson model for managing educational lessons
    """
    class Subject(models.TextChoices):
        MATHEMATICS = 'mathematics', 'Mathematics'
        SCIENCE = 'science', 'Science'
        ENGLISH = 'english', 'English'
        HISTORY = 'history', 'History'
        GEOGRAPHY = 'geography', 'Geography'
        PHYSICAL_EDUCATION = 'physical_education', 'Physical Education'
        ART = 'art', 'Art'
        MUSIC = 'music', 'Music'
        COMPUTER_SCIENCE = 'computer_science', 'Computer Science'
        LANGUAGES = 'languages', 'Languages'
        OTHER = 'other', 'Other'
    
    class LessonType(models.TextChoices):
        LECTURE = 'lecture', 'Lecture'
        INTERACTIVE = 'interactive', 'Interactive'
        PRACTICAL = 'practical', 'Practical'
        ASSESSMENT = 'assessment', 'Assessment'
        REVIEW = 'review', 'Review'
        PROJECT_BASED = 'project_based', 'Project-Based'
        COLLABORATIVE = 'collaborative', 'Collaborative'
        OTHER = 'other', 'Other'
    
    class Difficulty(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'
        EXPERT = 'expert', 'Expert'
    
    title = models.CharField(max_length=200, help_text="Lesson title")
    description = models.TextField(help_text="Lesson description")
    subject = models.CharField(max_length=20, choices=Subject.choices, help_text="Subject area")
    grade_level = models.CharField(max_length=10, help_text="Target grade level")
    lesson_type = models.CharField(max_length=20, choices=LessonType.choices, help_text="Type of lesson")
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, default=Difficulty.INTERMEDIATE)
    duration_minutes = models.PositiveIntegerField(help_text="Estimated duration in minutes")
    learning_objectives = models.JSONField(default=list, help_text="List of learning objectives")
    prerequisites = models.JSONField(default=list, help_text="Prerequisites for this lesson")
    materials_required = models.JSONField(default=list, help_text="Materials needed for this lesson")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_lessons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['subject', 'grade_level', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.get_subject_display()} ({self.grade_level})"
    
    @property
    def total_materials(self):
        return self.materials.count()
    
    @property
    def total_assessments(self):
        return self.assessments.count()


class LessonPlan(models.Model):
    """
    Detailed lesson plan model
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='plans')
    plan_title = models.CharField(max_length=200, help_text="Plan title")
    plan_description = models.TextField(help_text="Detailed plan description")
    learning_outcomes = models.JSONField(default=list, help_text="Expected learning outcomes")
    activities = models.JSONField(default=list, help_text="List of activities and their descriptions")
    time_allocation = models.JSONField(default=dict, help_text="Time allocation for each activity")
    assessment_criteria = models.JSONField(default=list, help_text="Assessment criteria")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lesson Plan'
        verbose_name_plural = 'Lesson Plans'
        ordering = ['lesson', 'plan_title']
    
    def __str__(self):
        return f"{self.plan_title} - {self.lesson.title}"


class LessonMaterial(models.Model):
    """
    Lesson materials and resources
    """
    class MaterialType(models.TextChoices):
        DOCUMENT = 'document', 'Document'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
        IMAGE = 'image', 'Image'
        PRESENTATION = 'presentation', 'Presentation'
        WORKSHEET = 'worksheet', 'Worksheet'
        INTERACTIVE = 'interactive', 'Interactive Content'
        LINK = 'link', 'External Link'
        OTHER = 'other', 'Other'
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='materials')
    material_type = models.CharField(max_length=20, choices=MaterialType.choices)
    title = models.CharField(max_length=200, help_text="Material title")
    description = models.TextField(help_text="Material description")
    file_path = models.CharField(max_length=500, blank=True, help_text="Path to material file")
    url = models.URLField(blank=True, help_text="URL to external material")
    content = models.TextField(blank=True, help_text="Direct content or text")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lesson Material'
        verbose_name_plural = 'Lesson Materials'
        ordering = ['lesson', 'material_type', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.lesson.title}"


class LessonAssessment(models.Model):
    """
    Lesson assessment and evaluation tools
    """
    class AssessmentType(models.TextChoices):
        QUIZ = 'quiz', 'Quiz'
        TEST = 'test', 'Test'
        ASSIGNMENT = 'assignment', 'Assignment'
        PROJECT = 'project', 'Project'
        PRESENTATION = 'presentation', 'Presentation'
        PARTICIPATION = 'participation', 'Participation'
        OTHER = 'other', 'Other'
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assessments')
    assessment_type = models.CharField(max_length=20, choices=AssessmentType.choices)
    title = models.CharField(max_length=200, help_text="Assessment title")
    description = models.TextField(help_text="Assessment description")
    questions = models.JSONField(default=list, help_text="Assessment questions and content")
    scoring_criteria = models.JSONField(default=dict, help_text="Scoring criteria and rubrics")
    time_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Time limit in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lesson Assessment'
        verbose_name_plural = 'Lesson Assessments'
        ordering = ['lesson', 'assessment_type', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.lesson.title}"


class LessonSession(models.Model):
    """
    Individual lesson session instances
    """
    class SessionStatus(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        POSTPONED = 'postponed', 'Postponed'
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='sessions')
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='taught_sessions')
    scheduled_date = models.DateTimeField(help_text="Scheduled date and time")
    actual_start_time = models.DateTimeField(null=True, blank=True, help_text="Actual start time")
    actual_end_time = models.DateTimeField(null=True, blank=True, help_text="Actual end time")
    status = models.CharField(max_length=20, choices=SessionStatus.choices, default=SessionStatus.SCHEDULED)
    participants = models.JSONField(default=list, help_text="List of participating students")
    notes = models.TextField(blank=True, help_text="Session notes and observations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lesson Session'
        verbose_name_plural = 'Lesson Sessions'
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.lesson.title} - {self.scheduled_date.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def duration_minutes(self):
        if self.actual_start_time and self.actual_end_time:
            return (self.actual_end_time - self.actual_start_time).total_seconds() / 60
        return None
    
    @property
    def is_overdue(self):
        if self.status == self.SessionStatus.SCHEDULED:
            return timezone.now() > self.scheduled_date
        return False


class LessonProgress(models.Model):
    """
    Student progress tracking for lessons
    """
    class ProgressStatus(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not Started'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        NEEDS_REVIEW = 'needs_review', 'Needs Review'
        MASTERED = 'mastered', 'Mastered'
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='student_progress')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='lesson_progress')
    progress_status = models.CharField(max_length=20, choices=ProgressStatus.choices, default=ProgressStatus.NOT_STARTED)
    completion_percentage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)], help_text="Completion percentage")
    time_spent_minutes = models.PositiveIntegerField(default=0, help_text="Time spent on lesson in minutes")
    last_accessed = models.DateTimeField(auto_now=True, help_text="Last time lesson was accessed")
    assessment_scores = models.JSONField(default=dict, help_text="Assessment scores and results")
    notes = models.TextField(blank=True, help_text="Student notes and feedback")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lesson Progress'
        verbose_name_plural = 'Lesson Progress Records'
        unique_together = ['lesson', 'student']
        ordering = ['lesson', 'student']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.lesson.title} ({self.get_progress_status_display()})"
