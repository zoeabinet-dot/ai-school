from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    WebcamSession, FrameAnalysis, BehaviorEvent, PrivacySettings, MonitoringAlert
)
from students.serializers import StudentSerializer

User = get_user_model()


class WebcamSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for WebcamSession model
    """
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='student'),
        source='student',
        write_only=True
    )
    session_type_display = serializers.CharField(source='get_session_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = WebcamSession
        fields = [
            'id', 'student', 'student_id', 'session_type', 'session_type_display',
            'start_time', 'end_time', 'duration', 'duration_formatted', 'status',
            'status_display', 'recording_quality', 'frame_rate', 'resolution',
            'storage_path', 'privacy_level', 'consent_given', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'start_time', 'created_at', 'updated_at']
    
    def get_duration_formatted(self, obj):
        """Format duration in human-readable format"""
        if obj.duration:
            hours = int(obj.duration // 60)
            minutes = int(obj.duration % 60)
            if hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        return "0m"
    
    def validate_recording_quality(self, value):
        """Ensure recording quality is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Recording quality must be between 0 and 100")
        return value
    
    def validate_frame_rate(self, value):
        """Ensure frame rate is within reasonable bounds"""
        if value is not None and (value < 1 or value > 60):
            raise serializers.ValidationError("Frame rate must be between 1 and 60 fps")
        return value
    
    def validate_resolution(self, value):
        """Validate resolution format"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Resolution must be a dictionary with width and height")
        return value
    
    def validate(self, data):
        """Validate session data"""
        if data.get('end_time') and data.get('start_time'):
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError("End time must be after start time")
        
        return data


class FrameAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for FrameAnalysis model
    """
    session = WebcamSessionSerializer(read_only=True)
    session_id = serializers.PrimaryKeyRelatedField(
        queryset=WebcamSession.objects.all(),
        source='session',
        write_only=True
    )
    analysis_type_display = serializers.CharField(source='get_analysis_type_display', read_only=True)
    
    class Meta:
        model = FrameAnalysis
        fields = [
            'id', 'session', 'session_id', 'timestamp', 'frame_number',
            'analysis_type', 'analysis_type_display', 'confidence_score',
            'detected_objects', 'facial_expressions', 'attention_metrics',
            'behavior_indicators', 'emotion_analysis', 'posture_analysis',
            'gaze_tracking', 'processing_time', 'ai_model_used', 'raw_data',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'timestamp', 'created_at', 'updated_at']
    
    def validate_confidence_score(self, value):
        """Ensure confidence score is within valid range"""
        if value is not None and (value < 0 or value > 1):
            raise serializers.ValidationError("Confidence score must be between 0 and 1")
        return value
    
    def validate_processing_time(self, value):
        """Ensure processing time is within reasonable bounds"""
        if value is not None and (value < 0 or value > 10000):  # Max 10 seconds
            raise serializers.ValidationError("Processing time must be between 0 and 10000 milliseconds")
        return value
    
    def validate_detected_objects(self, value):
        """Validate detected objects data"""
        if value and not isinstance(value, list):
            raise serializers.ValidationError("Detected objects must be a list")
        return value
    
    def validate_facial_expressions(self, value):
        """Validate facial expressions data"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Facial expressions must be a dictionary")
        return value
    
    def validate_attention_metrics(self, value):
        """Validate attention metrics data"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Attention metrics must be a dictionary")
        return value


class BehaviorEventSerializer(serializers.ModelSerializer):
    """
    Serializer for BehaviorEvent model
    """
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='student'),
        source='student',
        write_only=True
    )
    session = WebcamSessionSerializer(read_only=True)
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    
    class Meta:
        model = BehaviorEvent
        fields = [
            'id', 'student', 'student_id', 'session', 'timestamp', 'event_type',
            'event_type_display', 'severity', 'severity_display', 'description',
            'confidence_score', 'location', 'duration', 'triggers',
            'intervention_required', 'intervention_applied', 'outcome',
            'ai_analysis', 'manual_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'timestamp', 'created_at', 'updated_at']
    
    def validate_confidence_score(self, value):
        """Ensure confidence score is within valid range"""
        if value is not None and (value < 0 or value > 1):
            raise serializers.ValidationError("Confidence score must be between 0 and 1")
        return value
    
    def validate_duration(self, value):
        """Ensure duration is within reasonable bounds"""
        if value is not None and (value < 0 or value > 3600):  # Max 1 hour
            raise serializers.ValidationError("Duration must be between 0 and 3600 seconds")
        return value
    
    def validate_location(self, value):
        """Validate location data"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Location must be a dictionary")
        return value
    
    def validate_triggers(self, value):
        """Validate triggers data"""
        if value and not isinstance(value, list):
            raise serializers.ValidationError("Triggers must be a list")
        return value
    
    def validate_ai_analysis(self, value):
        """Validate AI analysis data"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("AI analysis must be a dictionary")
        return value


class PrivacySettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for PrivacySettings model
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    data_retention_display = serializers.CharField(source='get_data_retention_display', read_only=True)
    sharing_level_display = serializers.CharField(source='get_sharing_level_display', read_only=True)
    
    class Meta:
        model = PrivacySettings
        fields = [
            'id', 'user', 'webcam_monitoring_consent', 'data_collection_consent',
            'ai_analysis_consent', 'data_sharing_consent', 'data_retention',
            'data_retention_display', 'sharing_level', 'sharing_level_display',
            'third_party_access', 'data_export_consent', 'notification_preferences',
            'privacy_level', 'custom_settings', 'last_updated', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'last_updated', 'created_at', 'updated_at']
    
    def validate_privacy_level(self, value):
        """Ensure privacy level is within valid range"""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Privacy level must be between 1 and 5")
        return value
    
    def validate_custom_settings(self, value):
        """Validate custom settings data"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Custom settings must be a dictionary")
        return value
    
    def validate_notification_preferences(self, value):
        """Validate notification preferences data"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Notification preferences must be a dictionary")
        return value


class MonitoringAlertSerializer(serializers.ModelSerializer):
    """
    Serializer for MonitoringAlert model
    """
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='student'),
        source='student',
        write_only=True
    )
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = MonitoringAlert
        fields = [
            'id', 'student', 'student_id', 'timestamp', 'alert_type',
            'alert_type_display', 'severity', 'severity_display', 'status',
            'status_display', 'message', 'description', 'triggering_event',
            'location', 'duration', 'acknowledged_by', 'acknowledged_at',
            'resolution_notes', 'escalation_level', 'notification_sent',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'timestamp', 'created_at', 'updated_at']
    
    def validate_escalation_level(self, value):
        """Ensure escalation level is within valid range"""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Escalation level must be between 1 and 5")
        return value
    
    def validate_duration(self, value):
        """Ensure duration is within reasonable bounds"""
        if value is not None and (value < 0 or value > 86400):  # Max 24 hours
            raise serializers.ValidationError("Duration must be between 0 and 86400 seconds")
        return value
    
    def validate_location(self, value):
        """Validate location data"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Location must be a dictionary")
        return value


class StudentMonitoringDashboardSerializer(serializers.Serializer):
    """
    Serializer for comprehensive student monitoring dashboard
    """
    student = serializers.DictField()
    recent_sessions = WebcamSessionSerializer(many=True)
    recent_events = BehaviorEventSerializer(many=True)
    active_alerts = MonitoringAlertSerializer(many=True)
    privacy_settings = PrivacySettingsSerializer()
    monitoring_statistics = serializers.DictField()
    
    class Meta:
        fields = [
            'student', 'recent_sessions', 'recent_events',
            'active_alerts', 'privacy_settings', 'monitoring_statistics'
        ]


class BehaviorAnalysisSerializer(serializers.Serializer):
    """
    Serializer for behavior analysis results
    """
    student_id = serializers.IntegerField()
    session_id = serializers.IntegerField(required=False)
    analysis_type = serializers.CharField()
    analysis_result = serializers.DictField()
    timestamp = serializers.DateTimeField()
    
    class Meta:
        fields = ['student_id', 'session_id', 'analysis_type', 'analysis_result', 'timestamp']


class PrivacyComplianceSerializer(serializers.Serializer):
    """
    Serializer for privacy compliance reports
    """
    compliance_report = serializers.DictField()
    timestamp = serializers.DateTimeField()
    
    class Meta:
        fields = ['compliance_report', 'timestamp']


class RealTimeMonitoringSerializer(serializers.Serializer):
    """
    Serializer for real-time monitoring data
    """
    session_id = serializers.IntegerField()
    status = serializers.CharField()
    message = serializers.CharField()
    note = serializers.CharField()
    
    class Meta:
        fields = ['session_id', 'status', 'message', 'note']


class MonitoringFilterSerializer(serializers.Serializer):
    """
    Serializer for monitoring data filtering
    """
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="List of student IDs to filter by"
    )
    session_types = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of session types to filter by"
    )
    date_from = serializers.DateField(required=False, help_text="Start date for filtering")
    date_to = serializers.DateField(required=False, help_text="End date for filtering")
    event_types = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of event types to filter by"
    )
    severity_levels = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of severity levels to filter by"
    )
    
    def validate_date_range(self, data):
        """Validate date range"""
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError("Start date must be before end date")
        
        return data


class MonitoringExportSerializer(serializers.Serializer):
    """
    Serializer for monitoring data export requests
    """
    format = serializers.ChoiceField(choices=['json', 'csv', 'xlsx'], default='json')
    filters = MonitoringFilterSerializer(required=False)
    include_fields = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of fields to include in export"
    )
    date_range = serializers.DictField(required=False, help_text="Date range for export")
    
    def validate_format(self, value):
        """Validate export format"""
        if value not in ['json', 'csv', 'xlsx']:
            raise serializers.ValidationError("Unsupported export format")
        return value
    
    def validate_date_range(self, value):
        """Validate date range"""
        if value:
            start_date = value.get('start_date')
            end_date = value.get('end_date')
            
            if start_date and end_date:
                try:
                    start = datetime.strptime(start_date, '%Y-%m-%d').date()
                    end = datetime.strptime(end_date, '%Y-%m-%d').date()
                    if start >= end:
                        raise serializers.ValidationError("Start date must be before end date")
                except ValueError:
                    raise serializers.ValidationError("Invalid date format. Use YYYY-MM-DD")
        
        return value