from django.db import models
from django.utils import timezone
from accounts.models import Student, Staff, User
from learning.models import Lesson, Subject


class WebcamSession(models.Model):
    """Webcam monitoring sessions for students"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('terminated', 'Terminated'),
        ('error', 'Error'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='webcam_sessions')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    
    session_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Session Details
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    
    # Technical Details
    video_quality = models.CharField(max_length=20, default='720p')
    frame_rate = models.IntegerField(default=30)
    device_info = models.JSONField(default=dict)
    
    # Privacy and Consent
    consent_given = models.BooleanField(default=False)
    consent_timestamp = models.DateTimeField(blank=True, null=True)
    privacy_settings = models.JSONField(default=dict)
    
    # Analysis Settings
    face_detection_enabled = models.BooleanField(default=True)
    emotion_analysis_enabled = models.BooleanField(default=True)
    attention_tracking_enabled = models.BooleanField(default=True)
    posture_analysis_enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - Session {self.session_id}"


class AttentionAnalysis(models.Model):
    """Real-time attention analysis from webcam data"""
    
    ATTENTION_LEVEL_CHOICES = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ]
    
    GAZE_DIRECTION_CHOICES = [
        ('center', 'Looking at Screen'),
        ('left', 'Looking Left'),
        ('right', 'Looking Right'),
        ('up', 'Looking Up'),
        ('down', 'Looking Down'),
        ('away', 'Looking Away'),
    ]
    
    webcam_session = models.ForeignKey(WebcamSession, on_delete=models.CASCADE, related_name='attention_data')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Attention Metrics
    attention_level = models.CharField(max_length=20, choices=ATTENTION_LEVEL_CHOICES)
    attention_score = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100
    focus_duration_seconds = models.IntegerField()
    distraction_count = models.IntegerField(default=0)
    
    # Gaze Analysis
    gaze_direction = models.CharField(max_length=20, choices=GAZE_DIRECTION_CHOICES)
    eye_contact_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    blink_rate = models.IntegerField(blank=True, null=True)  # blinks per minute
    
    # Head Position
    head_pose = models.JSONField(default=dict)  # pitch, yaw, roll angles
    head_movement_intensity = models.CharField(max_length=20, default='normal')
    
    # Analysis Metadata
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2)
    analysis_method = models.CharField(max_length=50, default='computer_vision')
    
    def __str__(self):
        return f"{self.webcam_session.student.user.get_full_name()} - {self.attention_level} ({self.timestamp})"


class EmotionAnalysis(models.Model):
    """Emotion detection and analysis from facial expressions"""
    
    DOMINANT_EMOTION_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('surprised', 'Surprised'),
        ('fearful', 'Fearful'),
        ('disgusted', 'Disgusted'),
        ('neutral', 'Neutral'),
        ('confused', 'Confused'),
        ('frustrated', 'Frustrated'),
        ('excited', 'Excited'),
        ('bored', 'Bored'),
    ]
    
    ENGAGEMENT_LEVEL_CHOICES = [
        ('disengaged', 'Disengaged'),
        ('low', 'Low Engagement'),
        ('moderate', 'Moderate Engagement'),
        ('high', 'High Engagement'),
        ('very_high', 'Very High Engagement'),
    ]
    
    webcam_session = models.ForeignKey(WebcamSession, on_delete=models.CASCADE, related_name='emotion_data')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Emotion Detection
    dominant_emotion = models.CharField(max_length=20, choices=DOMINANT_EMOTION_CHOICES)
    emotion_scores = models.JSONField(default=dict)  # All emotion probabilities
    emotion_confidence = models.DecimalField(max_digits=3, decimal_places=2)
    
    # Engagement Analysis
    engagement_level = models.CharField(max_length=20, choices=ENGAGEMENT_LEVEL_CHOICES)
    engagement_score = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100
    
    # Facial Features
    facial_landmarks = models.JSONField(default=dict, blank=True)
    micro_expressions = models.JSONField(default=list, blank=True)
    
    # Learning Indicators
    confusion_detected = models.BooleanField(default=False)
    frustration_detected = models.BooleanField(default=False)
    comprehension_indicators = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.webcam_session.student.user.get_full_name()} - {self.dominant_emotion} ({self.timestamp})"


class BehaviorAnalysis(models.Model):
    """Behavioral pattern analysis from webcam data"""
    
    BEHAVIOR_TYPE_CHOICES = [
        ('focused', 'Focused Learning'),
        ('distracted', 'Distracted'),
        ('fidgeting', 'Fidgeting'),
        ('sleepy', 'Showing Signs of Fatigue'),
        ('engaged', 'Actively Engaged'),
        ('passive', 'Passive Learning'),
        ('confused', 'Showing Confusion'),
        ('confident', 'Showing Confidence'),
    ]
    
    webcam_session = models.ForeignKey(WebcamSession, on_delete=models.CASCADE, related_name='behavior_data')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Behavior Classification
    behavior_type = models.CharField(max_length=20, choices=BEHAVIOR_TYPE_CHOICES)
    behavior_intensity = models.CharField(max_length=20, default='moderate')  # mild, moderate, intense
    duration_seconds = models.IntegerField()
    
    # Movement Analysis
    body_movement_level = models.CharField(max_length=20, default='normal')  # minimal, normal, excessive
    posture_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)  # 0-1
    posture_changes = models.IntegerField(default=0)
    
    # Activity Detection
    hand_gestures = models.JSONField(default=list, blank=True)
    note_taking_detected = models.BooleanField(default=False)
    device_interaction = models.BooleanField(default=False)
    
    # Learning Behavior
    question_asking_gesture = models.BooleanField(default=False)
    thinking_posture = models.BooleanField(default=False)
    active_participation = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.webcam_session.student.user.get_full_name()} - {self.behavior_type} ({self.timestamp})"


class AlertEvent(models.Model):
    """Automated alerts based on webcam analysis"""
    
    ALERT_TYPE_CHOICES = [
        ('attention_drop', 'Attention Level Drop'),
        ('prolonged_confusion', 'Prolonged Confusion'),
        ('disengagement', 'Student Disengagement'),
        ('fatigue', 'Signs of Fatigue'),
        ('distraction', 'Persistent Distraction'),
        ('technical_issue', 'Technical Issue'),
        ('privacy_concern', 'Privacy Concern'),
        ('help_needed', 'Student Needs Help'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    webcam_session = models.ForeignKey(WebcamSession, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Alert Details
    message = models.TextField()
    trigger_data = models.JSONField(default=dict)  # Data that triggered the alert
    recommendations = models.JSONField(default=list)
    
    # Response Tracking
    acknowledged_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    acknowledged_at = models.DateTimeField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolution_notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    triggered_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.webcam_session.student.user.get_full_name()} - {self.get_alert_type_display()}"


class MonitoringSettings(models.Model):
    """Webcam monitoring settings and preferences"""
    
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='monitoring_settings')
    
    # Privacy Settings
    monitoring_enabled = models.BooleanField(default=False)
    parent_consent = models.BooleanField(default=False)
    student_consent = models.BooleanField(default=False)
    data_retention_days = models.IntegerField(default=30)
    
    # Analysis Settings
    face_detection = models.BooleanField(default=True)
    emotion_analysis = models.BooleanField(default=True)
    attention_tracking = models.BooleanField(default=True)
    behavior_analysis = models.BooleanField(default=False)
    posture_monitoring = models.BooleanField(default=False)
    
    # Alert Settings
    real_time_alerts = models.BooleanField(default=True)
    alert_thresholds = models.JSONField(default=dict)
    notification_preferences = models.JSONField(default=dict)
    
    # Recording Settings
    save_recordings = models.BooleanField(default=False)
    recording_quality = models.CharField(max_length=20, default='medium')
    auto_delete_recordings = models.BooleanField(default=True)
    
    # Schedule Settings
    monitoring_schedule = models.JSONField(default=dict)  # Days and times when monitoring is active
    break_intervals = models.JSONField(default=list)  # Scheduled breaks from monitoring
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - Monitoring Settings"


class MonitoringReport(models.Model):
    """Periodic reports on webcam monitoring data"""
    
    REPORT_TYPE_CHOICES = [
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
        ('session', 'Session Report'),
        ('custom', 'Custom Report'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='monitoring_reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    
    # Report Period
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Summary Statistics
    total_monitoring_time_minutes = models.IntegerField()
    average_attention_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dominant_emotions = models.JSONField(default=dict)
    behavior_patterns = models.JSONField(default=dict)
    
    # Key Insights
    attention_trends = models.JSONField(default=dict)
    engagement_patterns = models.JSONField(default=dict)
    learning_indicators = models.JSONField(default=dict)
    improvement_areas = models.JSONField(default=list)
    
    # Alerts Summary
    total_alerts = models.IntegerField(default=0)
    alert_breakdown = models.JSONField(default=dict)
    resolved_alerts = models.IntegerField(default=0)
    
    # Recommendations
    ai_recommendations = models.JSONField(default=list)
    intervention_suggestions = models.JSONField(default=list)
    
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.CharField(max_length=50, default='AI_Monitoring_System')
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.get_report_type_display()} ({self.start_date.date()})"


class PrivacyAuditLog(models.Model):
    """Audit log for privacy and data access"""
    
    ACTION_TYPE_CHOICES = [
        ('data_access', 'Data Access'),
        ('data_export', 'Data Export'),
        ('data_deletion', 'Data Deletion'),
        ('consent_given', 'Consent Given'),
        ('consent_revoked', 'Consent Revoked'),
        ('settings_changed', 'Settings Changed'),
        ('report_generated', 'Report Generated'),
        ('alert_triggered', 'Alert Triggered'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='privacy_audit_logs')
    action_type = models.CharField(max_length=30, choices=ACTION_TYPE_CHOICES)
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Action Details
    description = models.TextField()
    data_accessed = models.JSONField(default=list)  # What data was accessed/modified
    justification = models.TextField(blank=True, null=True)
    
    # Technical Details
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    session_id = models.CharField(max_length=100, blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.get_action_type_display()} by {self.performed_by.username}"