from django.db import models
from django.utils import timezone
from accounts.models import Student, Staff, Family, User
from learning.models import Subject, Lesson, LearningPath, Quiz


class StudentPerformanceMetrics(models.Model):
    """Comprehensive student performance tracking"""
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='performance_metrics')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    
    # Academic Performance
    overall_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    quiz_average = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    assignment_average = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    participation_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Learning Analytics
    lessons_completed = models.IntegerField(default=0)
    total_study_time_minutes = models.IntegerField(default=0)
    average_session_duration_minutes = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    concepts_mastered = models.IntegerField(default=0)
    concepts_struggling = models.IntegerField(default=0)
    
    # Engagement Metrics
    ai_interactions_count = models.IntegerField(default=0)
    questions_asked = models.IntegerField(default=0)
    help_requests = models.IntegerField(default=0)
    peer_collaborations = models.IntegerField(default=0)
    
    # Behavioral Indicators
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    punctuality_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    engagement_level = models.CharField(max_length=20, default='medium')  # low, medium, high
    motivation_level = models.CharField(max_length=20, default='medium')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'subject', 'date']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject.name} ({self.date})"


class LearningProgressTracker(models.Model):
    """Track learning progress over time"""
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress_tracking')
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE)
    
    # Progress Metrics
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    lessons_completed = models.IntegerField(default=0)
    total_lessons = models.IntegerField()
    current_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    
    # Performance Metrics
    average_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mastery_level = models.CharField(max_length=20, default='developing')  # developing, proficient, mastered
    learning_velocity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # lessons per week
    
    # Time Metrics
    total_time_spent_minutes = models.IntegerField(default=0)
    estimated_completion_date = models.DateField(blank=True, null=True)
    started_at = models.DateTimeField()
    last_activity = models.DateTimeField(auto_now=True)
    
    # Difficulty Adjustments
    difficulty_adjustments = models.JSONField(default=list)  # Track AI difficulty changes
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.learning_path.name} ({self.completion_percentage}%)"


class AttendanceRecord(models.Model):
    """Student attendance tracking"""
    
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused Absence'),
        ('partial', 'Partial Attendance'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    check_in_time = models.TimeField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)
    total_minutes = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'date']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.date} ({self.status})"


class BehavioralObservation(models.Model):
    """Track behavioral observations and patterns"""
    
    BEHAVIOR_TYPE_CHOICES = [
        ('positive', 'Positive Behavior'),
        ('concerning', 'Concerning Behavior'),
        ('neutral', 'Neutral Observation'),
        ('achievement', 'Achievement/Milestone'),
        ('social', 'Social Interaction'),
        ('academic', 'Academic Behavior'),
    ]
    
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('significant', 'Significant'),
        ('critical', 'Critical'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='behavioral_observations')
    observer = models.ForeignKey(User, on_delete=models.CASCADE)  # Staff or AI system
    behavior_type = models.CharField(max_length=20, choices=BEHAVIOR_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, blank=True, null=True)
    description = models.TextField()
    context = models.TextField(blank=True, null=True)  # Situation/context
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    intervention_needed = models.BooleanField(default=False)
    follow_up_required = models.BooleanField(default=False)
    tags = models.JSONField(default=list)
    observed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.get_behavior_type_display()} ({self.observed_at.date()})"


class EngagementMetrics(models.Model):
    """Track student engagement across different activities"""
    
    ACTIVITY_TYPE_CHOICES = [
        ('lesson', 'Lesson'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('discussion', 'Discussion'),
        ('project', 'Project'),
        ('ai_interaction', 'AI Interaction'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='engagement_metrics')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    
    # Engagement Scores (0-100)
    attention_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    participation_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    interaction_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    completion_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Time Metrics
    time_spent_minutes = models.IntegerField()
    expected_time_minutes = models.IntegerField(blank=True, null=True)
    
    # Behavioral Indicators
    clicks_interactions = models.IntegerField(default=0)
    questions_asked = models.IntegerField(default=0)
    help_requests = models.IntegerField(default=0)
    off_task_minutes = models.IntegerField(default=0)
    
    session_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.activity_type} ({self.session_date.date()})"


class LearningAnalytics(models.Model):
    """Advanced learning analytics and insights"""
    
    ANALYTICS_TYPE_CHOICES = [
        ('learning_style', 'Learning Style Analysis'),
        ('knowledge_gap', 'Knowledge Gap Analysis'),
        ('progress_prediction', 'Progress Prediction'),
        ('difficulty_analysis', 'Difficulty Analysis'),
        ('engagement_pattern', 'Engagement Pattern'),
        ('performance_trend', 'Performance Trend'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='learning_analytics')
    analytics_type = models.CharField(max_length=30, choices=ANALYTICS_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    
    # Analysis Results
    insights = models.JSONField(default=dict)
    recommendations = models.JSONField(default=list)
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    
    # Data Sources
    data_points_analyzed = models.IntegerField()
    analysis_period_start = models.DateField()
    analysis_period_end = models.DateField()
    
    # Metadata
    algorithm_version = models.CharField(max_length=20, default='1.0')
    generated_by = models.CharField(max_length=50, default='AI_Analytics_Engine')
    is_actionable = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.get_analytics_type_display()}"


class ClassroomAnalytics(models.Model):
    """Aggregate analytics for classroom/grade level"""
    
    grade_level = models.CharField(max_length=5)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    analysis_date = models.DateField(default=timezone.now)
    
    # Performance Metrics
    average_performance = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    performance_distribution = models.JSONField(default=dict)  # Grade distribution
    top_performers_count = models.IntegerField(default=0)
    struggling_students_count = models.IntegerField(default=0)
    
    # Engagement Metrics
    average_engagement = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    participation_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Learning Progress
    concepts_mastered = models.JSONField(default=list)
    concepts_struggling = models.JSONField(default=list)
    common_misconceptions = models.JSONField(default=list)
    
    # AI Insights
    ai_recommendations = models.JSONField(default=list)
    intervention_suggestions = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['grade_level', 'subject', 'analysis_date']
    
    def __str__(self):
        return f"Grade {self.grade_level} - {self.subject.name} ({self.analysis_date})"


class ParentEngagementMetrics(models.Model):
    """Track family/parent engagement with the platform"""
    
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='engagement_metrics')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='family_engagement')
    date = models.DateField(default=timezone.now)
    
    # Platform Engagement
    login_count = models.IntegerField(default=0)
    session_duration_minutes = models.IntegerField(default=0)
    pages_viewed = models.IntegerField(default=0)
    
    # Communication Metrics
    messages_sent = models.IntegerField(default=0)
    messages_received = models.IntegerField(default=0)
    notifications_read = models.IntegerField(default=0)
    
    # Monitoring Activity
    progress_checks = models.IntegerField(default=0)
    report_views = models.IntegerField(default=0)
    assignment_reviews = models.IntegerField(default=0)
    
    # Support Actions
    help_requests = models.IntegerField(default=0)
    meeting_requests = models.IntegerField(default=0)
    feedback_provided = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['family', 'student', 'date']
    
    def __str__(self):
        return f"{self.family.user.get_full_name()} - {self.student.user.get_full_name()} ({self.date})"


class SystemAnalytics(models.Model):
    """System-wide analytics and metrics"""
    
    METRIC_TYPE_CHOICES = [
        ('performance', 'System Performance'),
        ('usage', 'Usage Statistics'),
        ('engagement', 'Engagement Metrics'),
        ('ai_effectiveness', 'AI Effectiveness'),
        ('learning_outcomes', 'Learning Outcomes'),
    ]
    
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPE_CHOICES)
    date = models.DateField(default=timezone.now)
    
    # Metrics Data
    metrics = models.JSONField(default=dict)
    trends = models.JSONField(default=dict)
    comparisons = models.JSONField(default=dict)  # Week-over-week, month-over-month
    
    # System Health
    uptime_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    response_time_ms = models.IntegerField(blank=True, null=True)
    error_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Usage Statistics
    active_users = models.IntegerField(blank=True, null=True)
    total_sessions = models.IntegerField(blank=True, null=True)
    average_session_duration = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['metric_type', 'date']
    
    def __str__(self):
        return f"{self.get_metric_type_display()} - {self.date}"