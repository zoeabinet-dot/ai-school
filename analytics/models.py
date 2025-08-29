from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class LearningAnalytics(models.Model):
    """
    Comprehensive learning analytics and metrics
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_analytics')
    
    # Time-based metrics
    date = models.DateField()
    total_learning_time = models.IntegerField(help_text="Total learning time in minutes")
    active_learning_time = models.IntegerField(help_text="Active/engaged learning time in minutes")
    
    # Session metrics
    sessions_started = models.IntegerField(default=0)
    sessions_completed = models.IntegerField(default=0)
    sessions_abandoned = models.IntegerField(default=0)
    
    # Performance metrics
    average_attention_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    average_engagement_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    # Subject-specific metrics
    subject_performance = models.JSONField(default=dict, help_text="Performance by subject")
    skill_progress = models.JSONField(default=dict, help_text="Progress by skill area")
    
    # AI interaction metrics
    ai_conversations_count = models.IntegerField(default=0)
    ai_recommendations_followed = models.IntegerField(default=0)
    ai_lessons_completed = models.IntegerField(default=0)
    
    # Behavioral insights
    learning_patterns = models.JSONField(default=dict, blank=True)
    attention_trends = models.JSONField(default=list, blank=True)
    engagement_peaks = models.JSONField(default=list, blank=True)
    
    # Quality metrics
    data_quality_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=100
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'learning_analytics'
        unique_together = ['student', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"Learning Analytics for {self.student.get_full_name()} on {self.date}"


class PerformanceMetrics(models.Model):
    """
    Detailed performance metrics and KPIs
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performance_metrics')
    
    # Academic performance
    overall_gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        blank=True, null=True
    )
    
    subject_grades = models.JSONField(default=dict, help_text="Grades by subject")
    improvement_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Percentage improvement over time",
        blank=True, null=True
    )
    
    # Learning efficiency
    learning_speed = models.CharField(max_length=20, choices=[
        ('slow', 'Slow'),
        ('average', 'Average'),
        ('fast', 'Fast'),
        ('accelerated', 'Accelerated'),
    ], blank=True, null=True)
    
    retention_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Information retention percentage",
        blank=True, null=True
    )
    
    # Goal achievement
    goals_set = models.IntegerField(default=0)
    goals_achieved = models.IntegerField(default=0)
    goal_success_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    # Comparative metrics
    peer_percentile = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Performance percentile compared to peers",
        blank=True, null=True
    )
    
    grade_level_percentile = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Performance percentile within grade level",
        blank=True, null=True
    )
    
    # AI insights
    ai_learning_recommendations = models.JSONField(default=list, blank=True)
    predicted_performance = models.JSONField(default=dict, blank=True)
    
    # Time period
    period_start = models.DateField()
    period_end = models.DateField()
    period_type = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semester', 'Semester'),
        ('yearly', 'Yearly'),
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'performance_metrics'
        unique_together = ['student', 'period_start', 'period_end', 'period_type']
        ordering = ['-period_end']
    
    def __str__(self):
        return f"Performance Metrics for {self.student.get_full_name()} ({self.period_start} to {self.period_end})"


class EngagementAnalytics(models.Model):
    """
    Student engagement and participation analytics
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='engagement_analytics')
    
    # Engagement metrics
    date = models.DateField()
    total_engagement_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Activity breakdown
    lesson_engagement = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    project_engagement = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    social_engagement = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Time-based engagement
    morning_engagement = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    afternoon_engagement = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    evening_engagement = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    # Engagement patterns
    engagement_pattern = models.CharField(max_length=50, choices=[
        ('consistent', 'Consistent'),
        ('variable', 'Variable'),
        ('declining', 'Declining'),
        ('improving', 'Improving'),
        ('sporadic', 'Sporadic'),
    ])
    
    peak_engagement_hours = models.JSONField(default=list, blank=True)
    low_engagement_periods = models.JSONField(default=list, blank=True)
    
    # Behavioral indicators
    attention_span = models.IntegerField(help_text="Average attention span in minutes")
    distraction_frequency = models.IntegerField(default=0, help_text="Number of distractions detected")
    re_engagement_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Rate of re-engagement after distractions"
    )
    
    # AI insights
    engagement_recommendations = models.JSONField(default=list, blank=True)
    optimal_learning_times = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'engagement_analytics'
        unique_together = ['student', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"Engagement Analytics for {self.student.get_full_name()} on {self.date}"


class DashboardConfiguration(models.Model):
    """
    User-specific dashboard configurations and preferences
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dashboard_config')
    
    # Dashboard layout
    layout_type = models.CharField(max_length=20, choices=[
        ('grid', 'Grid Layout'),
        ('list', 'List Layout'),
        ('custom', 'Custom Layout'),
    ], default='grid')
    
    # Widget configurations
    enabled_widgets = models.JSONField(default=list, help_text="List of enabled dashboard widgets")
    widget_positions = models.JSONField(default=dict, help_text="Widget positions and sizes")
    widget_settings = models.JSONField(default=dict, help_text="Individual widget configurations")
    
    # Chart preferences
    preferred_chart_types = models.JSONField(default=list, help_text="Preferred chart types for data visualization")
    color_scheme = models.CharField(max_length=50, default='default', help_text="Dashboard color scheme")
    
    # Data preferences
    refresh_interval = models.IntegerField(default=300, help_text="Data refresh interval in seconds")
    data_range = models.CharField(max_length=20, choices=[
        ('1d', '1 Day'),
        ('1w', '1 Week'),
        ('1m', '1 Month'),
        ('3m', '3 Months'),
        ('6m', '6 Months'),
        ('1y', '1 Year'),
        ('all', 'All Time'),
    ], default='1m')
    
    # Notification settings
    notification_preferences = models.JSONField(default=dict, help_text="Dashboard notification preferences")
    alert_thresholds = models.JSONField(default=dict, help_text="Alert thresholds for various metrics")
    
    # Accessibility
    font_size = models.CharField(max_length=20, choices=[
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('extra_large', 'Extra Large'),
    ], default='medium')
    
    high_contrast = models.BooleanField(default=False)
    screen_reader_friendly = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'dashboard_configurations'
    
    def __str__(self):
        return f"Dashboard Configuration for {self.user.username}"


class ReportTemplate(models.Model):
    """
    Predefined report templates for different user roles
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Template metadata
    template_type = models.CharField(max_length=50, choices=[
        ('student_progress', 'Student Progress Report'),
        ('academic_performance', 'Academic Performance Report'),
        ('engagement_analysis', 'Engagement Analysis Report'),
        ('behavioral_summary', 'Behavioral Summary Report'),
        ('ai_insights', 'AI Insights Report'),
        ('comprehensive', 'Comprehensive Report'),
    ])
    
    target_audience = models.CharField(max_length=50, choices=[
        ('student', 'Student'),
        ('family', 'Family/Guardian'),
        ('staff', 'Staff/Teacher'),
        ('admin', 'Administrator'),
        ('all', 'All Users'),
    ])
    
    # Content configuration
    sections = models.JSONField(default=list, help_text="Report sections and their order")
    metrics_included = models.JSONField(default=list, help_text="Metrics to include in the report")
    visualizations = models.JSONField(default=list, help_text="Charts and graphs to include")
    
    # Formatting options
    include_charts = models.BooleanField(default=True)
    include_tables = models.BooleanField(default=True)
    include_summaries = models.BooleanField(default=True)
    include_recommendations = models.BooleanField(default=True)
    
    # Export options
    export_formats = models.JSONField(default=list, help_text="Available export formats")
    custom_styling = models.JSONField(default=dict, blank=True, help_text="Custom styling options")
    
    # Access control
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='created_report_templates'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'report_templates'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.get_template_type_display()}"
