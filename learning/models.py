from django.db import models
from django.utils import timezone
from accounts.models import Student, Staff, User


class Subject(models.Model):
    """Academic subjects"""
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    grade_levels = models.JSONField(default=list)  # List of applicable grade levels
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class LearningPath(models.Model):
    """Personalized learning paths for students"""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='learning_paths')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    estimated_duration_hours = models.IntegerField()
    prerequisites_met = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by_ai = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.name}"


class Lesson(models.Model):
    """Individual lessons within learning paths"""
    
    LESSON_TYPE_CHOICES = [
        ('video', 'Video Lesson'),
        ('reading', 'Reading Material'),
        ('interactive', 'Interactive Exercise'),
        ('quiz', 'Quiz/Assessment'),
        ('project', 'Project Work'),
        ('discussion', 'AI Discussion'),
    ]
    
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField()
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES)
    content = models.JSONField(default=dict)  # Flexible content structure
    order = models.IntegerField()
    estimated_duration_minutes = models.IntegerField()
    difficulty_level = models.CharField(max_length=20, choices=LearningPath.DIFFICULTY_CHOICES)
    learning_objectives = models.JSONField(default=list)
    resources = models.JSONField(default=list)  # URLs, files, etc.
    is_mandatory = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['learning_path', 'order']
        unique_together = ['learning_path', 'order']
    
    def __str__(self):
        return f"{self.learning_path.name} - {self.title}"


class LessonProgress(models.Model):
    """Track student progress on individual lessons"""
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('needs_review', 'Needs Review'),
        ('mastered', 'Mastered'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='student_progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # 0-100
    time_spent_minutes = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    last_accessed = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['student', 'lesson']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.lesson.title} ({self.status})"


class Assignment(models.Model):
    """Assignments and projects"""
    
    TYPE_CHOICES = [
        ('homework', 'Homework'),
        ('project', 'Project'),
        ('essay', 'Essay'),
        ('presentation', 'Presentation'),
        ('experiment', 'Experiment'),
        ('creative', 'Creative Work'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    assignment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    learning_path = models.ForeignKey(LearningPath, on_delete=models.SET_NULL, blank=True, null=True)
    assigned_to = models.ManyToManyField(Student, related_name='assignments')
    created_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='created_assignments')
    due_date = models.DateTimeField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    instructions = models.TextField()
    resources = models.JSONField(default=list)
    rubric = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.subject.name}"


class AssignmentSubmission(models.Model):
    """Student submissions for assignments"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('returned', 'Returned'),
        ('resubmitted', 'Resubmitted'),
    ]
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    content = models.TextField(blank=True, null=True)
    files = models.JSONField(default=list)  # File paths/URLs
    submitted_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    graded_at = models.DateTimeField(blank=True, null=True)
    is_late = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['assignment', 'student']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.assignment.title}"


class Quiz(models.Model):
    """Quizzes and assessments"""
    
    QUIZ_TYPE_CHOICES = [
        ('practice', 'Practice Quiz'),
        ('assessment', 'Assessment'),
        ('final', 'Final Exam'),
        ('diagnostic', 'Diagnostic Test'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)
    time_limit_minutes = models.IntegerField(blank=True, null=True)
    max_attempts = models.IntegerField(default=1)
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, default=70.00)
    is_randomized = models.BooleanField(default=False)
    show_results_immediately = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.subject.name}"


class Question(models.Model):
    """Questions for quizzes"""
    
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
        ('fill_blank', 'Fill in the Blank'),
        ('matching', 'Matching'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    options = models.JSONField(default=dict, blank=True)  # For multiple choice, matching, etc.
    correct_answer = models.JSONField(default=dict)
    explanation = models.TextField(blank=True, null=True)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    order = models.IntegerField()
    difficulty_level = models.CharField(max_length=20, choices=LearningPath.DIFFICULTY_CHOICES)
    
    class Meta:
        ordering = ['quiz', 'order']
        unique_together = ['quiz', 'order']
    
    def __str__(self):
        return f"{self.quiz.title} - Question {self.order}"


class QuizAttempt(models.Model):
    """Student quiz attempts"""
    
    STATUS_CHOICES = [
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('timed_out', 'Timed Out'),
        ('abandoned', 'Abandoned'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_attempts')
    attempt_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='started')
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total_points = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    answers = models.JSONField(default=dict)  # Question ID -> Answer
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    time_spent_minutes = models.IntegerField(blank=True, null=True)
    
    class Meta:
        unique_together = ['quiz', 'student', 'attempt_number']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.quiz.title} (Attempt {self.attempt_number})"


class StudentPortfolio(models.Model):
    """Student portfolio for showcasing work"""
    
    ITEM_TYPE_CHOICES = [
        ('project', 'Project'),
        ('artwork', 'Artwork'),
        ('writing', 'Writing Sample'),
        ('video', 'Video'),
        ('code', 'Code Project'),
        ('presentation', 'Presentation'),
        ('certificate', 'Certificate'),
        ('achievement', 'Achievement'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    files = models.JSONField(default=list)  # File paths/URLs
    tags = models.JSONField(default=list)
    reflection = models.TextField(blank=True, null=True)  # Student's reflection on the work
    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.title}"