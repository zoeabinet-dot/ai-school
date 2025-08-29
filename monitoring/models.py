from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class WebcamSession(models.Model):
    """
    Webcam monitoring sessions for student engagement tracking
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='webcam_sessions')
    
    # Session information
    session_id = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    
    # Session metadata
    lesson_id = models.CharField(max_length=100, blank=True, null=True)
    session_type = models.CharField(max_length=50, choices=[
        ('ai_lesson', 'AI Lesson'),
        ('video_lesson', 'Video Lesson'),
        ('quiz', 'Quiz'),
        ('project_work', 'Project Work'),
        ('reading', 'Reading'),
        ('practice', 'Practice Exercise'),
    ])
    
    # Privacy and consent
    consent_given = models.BooleanField(default=False)
    consent_timestamp = models.DateTimeField(blank=True, null=True)
    privacy_level = models.CharField(max_length=20, choices=[
        ('full', 'Full Monitoring'),
        ('partial', 'Partial Monitoring'),
        ('minimal', 'Minimal Monitoring'),
        ('none', 'No Monitoring'),
    ], default='partial')
    
    # Technical details
    device_info = models.JSONField(default=dict, blank=True)
    browser_info = models.JSONField(default=dict, blank=True)
    connection_quality = models.CharField(max_length=20, choices=[
        ('poor', 'Poor'),
        ('fair', 'Fair'),
        ('good', 'Good'),
        ('excellent', 'Excellent'),
    ], blank=True, null=True)
    
    # Session status
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('interrupted', 'Interrupted'),
        ('error', 'Error'),
    ], default='active')
    
    # Data quality
    frames_captured = models.IntegerField(default=0)
    analysis_quality = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'webcam_sessions'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"Webcam Session {self.session_id} for {self.student.get_full_name()}"


class FrameAnalysis(models.Model):
    """
    Individual frame analysis from webcam monitoring
    """
    session = models.ForeignKey(WebcamSession, on_delete=models.CASCADE, related_name='frame_analyses')
    
    # Frame information
    frame_number = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    frame_data_hash = models.CharField(max_length=64, blank=True, null=True)
    
    # Analysis results
    face_detected = models.BooleanField(default=False)
    face_count = models.IntegerField(default=0)
    face_locations = models.JSONField(default=list, blank=True)
    
    # Attention metrics
    attention_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    gaze_direction = models.CharField(max_length=50, choices=[
        ('screen', 'Looking at Screen'),
        ('away', 'Looking Away'),
        ('down', 'Looking Down'),
        ('up', 'Looking Up'),
        ('left', 'Looking Left'),
        ('right', 'Looking Right'),
        ('unknown', 'Unknown'),
    ], blank=True, null=True)
    
    gaze_confidence = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    # Emotional analysis
    emotional_state = models.CharField(max_length=50, choices=[
        ('happy', 'Happy'),
        ('focused', 'Focused'),
        ('frustrated', 'Frustrated'),
        ('bored', 'Bored'),
        ('confused', 'Confused'),
        ('excited', 'Excited'),
        ('neutral', 'Neutral'),
        ('unknown', 'Unknown'),
    ], blank=True, null=True)
    
    emotional_confidence = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    # Behavioral indicators
    head_pose = models.JSONField(default=dict, blank=True)
    eye_blink_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        blank=True, null=True
    )
    
    # AI model information
    ai_model_used = models.CharField(max_length=100, blank=True, null=True)
    processing_time_ms = models.IntegerField(blank=True, null=True)
    
    # Privacy compliance
    face_blurred = models.BooleanField(default=False)
    data_anonymized = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'frame_analyses'
        ordering = ['session', 'frame_number']
        unique_together = ['session', 'frame_number']
    
    def __str__(self):
        return f"Frame {self.frame_number} from Session {self.session.session_id}"


class BehaviorEvent(models.Model):
    """
    Significant behavioral events detected during monitoring
    """
    session = models.ForeignKey(WebcamSession, on_delete=models.CASCADE, related_name='behavior_events')
    
    # Event information
    event_type = models.CharField(max_length=50, choices=[
        ('attention_loss', 'Attention Loss'),
        ('distraction', 'Distraction Detected'),
        ('re_engagement', 'Re-engagement'),
        ('frustration', 'Frustration Detected'),
        ('boredom', 'Boredom Detected'),
        ('excitement', 'Excitement Detected'),
        ('confusion', 'Confusion Detected'),
        ('break', 'Break Taken'),
        ('return', 'Return from Break'),
        ('technical_issue', 'Technical Issue'),
        ('other', 'Other'),
    ])
    
    # Event details
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    duration_seconds = models.IntegerField(blank=True, null=True)
    
    # Event severity
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], default='medium')
    
    # Event description
    description = models.TextField(blank=True, null=True)
    context = models.JSONField(default=dict, blank=True)
    
    # AI analysis
    ai_confidence = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    ai_insights = models.JSONField(default=dict, blank=True)
    ai_recommendations = models.JSONField(default=list, blank=True)
    
    # Response tracking
    staff_notified = models.BooleanField(default=False)
    notification_sent = models.DateTimeField(blank=True, null=True)
    response_taken = models.CharField(max_length=100, blank=True, null=True)
    
    # Metadata
    frame_range = models.JSONField(default=list, blank=True)
    related_frames = models.ManyToManyField(FrameAnalysis, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'behavior_events'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.get_event_type_display()} for {self.session.student.get_full_name()} at {self.start_time}"
    
    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
            self.duration_seconds = int(duration)
        super().save(*args, **kwargs)


class PrivacySettings(models.Model):
    """
    User privacy settings and consent management
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='privacy_settings')
    
    # Monitoring consent
    webcam_monitoring_consent = models.BooleanField(default=False)
    webcam_consent_date = models.DateTimeField(blank=True, null=True)
    webcam_consent_version = models.CharField(max_length=20, blank=True, null=True)
    
    # Data collection consent
    behavioral_data_collection = models.BooleanField(default=False)
    academic_data_collection = models.BooleanField(default=False)
    ai_analysis_consent = models.BooleanField(default=False)
    
    # Data retention preferences
    data_retention_days = models.IntegerField(default=365, help_text="Days to retain personal data")
    anonymize_after_days = models.IntegerField(default=30, help_text="Days after which to anonymize data")
    
    # Sharing preferences
    share_with_family = models.BooleanField(default=True)
    share_with_staff = models.BooleanField(default=True)
    share_with_ai_system = models.BooleanField(default=True)
    share_for_research = models.BooleanField(default=False)
    
    # Notification preferences
    privacy_notifications = models.BooleanField(default=True)
    data_breach_alerts = models.BooleanField(default=True)
    consent_reminders = models.BooleanField(default=True)
    
    # Access control
    family_access_level = models.CharField(max_length=20, choices=[
        ('full', 'Full Access'),
        ('summary', 'Summary Only'),
        ('limited', 'Limited Access'),
        ('none', 'No Access'),
    ], default='summary')
    
    staff_access_level = models.CharField(max_length=20, choices=[
        ('full', 'Full Access'),
        ('summary', 'Summary Only'),
        ('limited', 'Limited Access'),
        ('none', 'No Access'),
    ], default='summary')
    
    # GDPR compliance
    gdpr_consent_given = models.BooleanField(default=False)
    gdpr_consent_date = models.DateTimeField(blank=True, null=True)
    right_to_forget = models.BooleanField(default=False)
    data_portability = models.BooleanField(default=True)
    
    # Audit trail
    consent_history = models.JSONField(default=list, blank=True)
    privacy_settings_changes = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'privacy_settings'
    
    def __str__(self):
        return f"Privacy Settings for {self.user.username}"


class MonitoringAlert(models.Model):
    """
    Alerts generated from monitoring data
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='monitoring_alerts')
    
    # Alert information
    alert_type = models.CharField(max_length=50, choices=[
        ('attention_loss', 'Attention Loss'),
        ('distraction', 'High Distraction'),
        ('frustration', 'Frustration Detected'),
        ('boredom', 'Boredom Detected'),
        ('technical_issue', 'Technical Issue'),
        ('privacy_concern', 'Privacy Concern'),
        ('behavior_change', 'Behavior Change'),
        ('performance_drop', 'Performance Drop'),
        ('engagement_decline', 'Engagement Decline'),
        ('other', 'Other'),
    ])
    
    # Alert details
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=[
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('alert', 'Alert'),
        ('critical', 'Critical'),
    ], default='info')
    
    # Alert metadata
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    
    # Alert context
    context_data = models.JSONField(default=dict, blank=True)
    related_sessions = models.JSONField(default=list, blank=True)
    related_events = models.JSONField(default=list, blank=True)
    
    # Recipients
    notify_family = models.BooleanField(default=True)
    notify_staff = models.BooleanField(default=True)
    notify_admin = models.BooleanField(default=False)
    
    # Response tracking
    acknowledged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='acknowledged_alerts'
    )
    acknowledged_at = models.DateTimeField(blank=True, null=True)
    response_notes = models.TextField(blank=True, null=True)
    
    # AI insights
    ai_analysis = models.JSONField(default=dict, blank=True)
    ai_recommendations = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'monitoring_alerts'
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"{self.alert_type} Alert for {self.student.get_full_name()} at {self.detected_at}"
