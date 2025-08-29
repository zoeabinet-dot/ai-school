from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    LearningAnalytics, PerformanceMetrics, EngagementAnalytics,
    DashboardConfiguration, ReportTemplate
)
from students.serializers import StudentSerializer

User = get_user_model()


class LearningAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for LearningAnalytics model
    """
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='student'),
        source='student',
        write_only=True
    )
    subject_display = serializers.CharField(source='get_subject_display', read_only=True)
    learning_style_display = serializers.CharField(source='get_learning_style_display', read_only=True)
    
    class Meta:
        model = LearningAnalytics
        fields = [
            'id', 'student', 'student_id', 'date', 'subject', 'subject_display',
            'total_learning_time', 'sessions_completed', 'lessons_completed',
            'subject_mastery_level', 'learning_style', 'learning_style_display',
            'difficulty_level', 'engagement_score', 'completion_rate',
            'ai_assistance_used', 'peer_interaction_time', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_total_learning_time(self, value):
        """Ensure learning time is within reasonable bounds"""
        if value is not None and (value < 0 or value > 1440):  # Max 24 hours
            raise serializers.ValidationError("Learning time must be between 0 and 1440 minutes")
        return value
    
    def validate_subject_mastery_level(self, value):
        """Ensure mastery level is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Mastery level must be between 0 and 100")
        return value
    
    def validate_engagement_score(self, value):
        """Ensure engagement score is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Engagement score must be between 0 and 100")
        return value
    
    def validate_completion_rate(self, value):
        """Ensure completion rate is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Completion rate must be between 0 and 100")
        return value


class PerformanceMetricsSerializer(serializers.ModelSerializer):
    """
    Serializer for PerformanceMetrics model
    """
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='student'),
        source='student',
        write_only=True
    )
    learning_speed_display = serializers.CharField(source='get_learning_speed_display', read_only=True)
    period_type_display = serializers.CharField(source='get_period_type_display', read_only=True)
    
    class Meta:
        model = PerformanceMetrics
        fields = [
            'id', 'student', 'student_id', 'period_start', 'period_end', 'period_type',
            'period_type_display', 'overall_grade', 'attendance_percentage',
            'homework_completion_rate', 'test_average', 'project_average',
            'participation_score', 'subject_grades', 'improvement_rate',
            'learning_speed', 'learning_speed_display', 'retention_rate',
            'goals_set', 'goals_achieved', 'goal_success_rate',
            'peer_percentile', 'grade_level_percentile',
            'ai_learning_recommendations', 'predicted_performance',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_overall_grade(self, value):
        """Ensure grade is within valid range"""
        if value is not None and (value < 0 or value > 4):
            raise serializers.ValidationError("Grade must be between 0 and 4")
        return value
    
    def validate_attendance_percentage(self, value):
        """Ensure attendance percentage is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Attendance percentage must be between 0 and 100")
        return value
    
    def validate_homework_completion_rate(self, value):
        """Ensure homework completion rate is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Homework completion rate must be between 0 and 100")
        return value
    
    def validate_test_average(self, value):
        """Ensure test average is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Test average must be between 0 and 100")
        return value
    
    def validate_project_average(self, value):
        """Ensure project average is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Project average must be between 0 and 100")
        return value
    
    def validate_participation_score(self, value):
        """Ensure participation score is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Participation score must be between 0 and 100")
        return value
    
    def validate_improvement_rate(self, value):
        """Ensure improvement rate is within valid range"""
        if value is not None and (value < -100 or value > 100):
            raise serializers.ValidationError("Improvement rate must be between -100 and 100")
        return value
    
    def validate_retention_rate(self, value):
        """Ensure retention rate is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Retention rate must be between 0 and 100")
        return value
    
    def validate_goal_success_rate(self, value):
        """Ensure goal success rate is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Goal success rate must be between 0 and 100")
        return value
    
    def validate_peer_percentile(self, value):
        """Ensure peer percentile is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Peer percentile must be between 0 and 100")
        return value
    
    def validate_grade_level_percentile(self, value):
        """Ensure grade level percentile is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Grade level percentile must be between 0 and 100")
        return value
    
    def validate(self, data):
        """Validate period dates"""
        period_start = data.get('period_start')
        period_end = data.get('period_end')
        
        if period_start and period_end and period_start >= period_end:
            raise serializers.ValidationError("Period start must be before period end")
        
        return data


class EngagementAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for EngagementAnalytics model
    """
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='student'),
        source='student',
        write_only=True
    )
    engagement_level_display = serializers.CharField(source='get_engagement_level_display', read_only=True)
    
    class Meta:
        model = EngagementAnalytics
        fields = [
            'id', 'student', 'student_id', 'date', 'total_engagement_score',
            'engagement_level', 'engagement_level_display', 'active_learning_time',
            'passive_learning_time', 'interactive_activities', 'collaboration_time',
            'self_directed_learning', 'participation_rate', 'retention_rate',
            'motivation_score', 'focus_metrics', 'break_patterns',
            'learning_preferences', 'engagement_trends', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_total_engagement_score(self, value):
        """Ensure engagement score is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Engagement score must be between 0 and 100")
        return value
    
    def validate_active_learning_time(self, value):
        """Ensure active learning time is within reasonable bounds"""
        if value is not None and (value < 0 or value > 1440):  # Max 24 hours
            raise serializers.ValidationError("Active learning time must be between 0 and 1440 minutes")
        return value
    
    def validate_passive_learning_time(self, value):
        """Ensure passive learning time is within reasonable bounds"""
        if value is not None and (value < 0 or value > 1440):  # Max 24 hours
            raise serializers.ValidationError("Passive learning time must be between 0 and 1440 minutes")
        return value
    
    def validate_participation_rate(self, value):
        """Ensure participation rate is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Participation rate must be between 0 and 100")
        return value
    
    def validate_retention_rate(self, value):
        """Ensure retention rate is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Retention rate must be between 0 and 100")
        return value
    
    def validate_motivation_score(self, value):
        """Ensure motivation score is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Motivation score must be between 0 and 100")
        return value


class DashboardConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer for DashboardConfiguration model
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    layout_display = serializers.CharField(source='get_layout_display', read_only=True)
    theme_display = serializers.CharField(source='get_theme_display', read_only=True)
    
    class Meta:
        model = DashboardConfiguration
        fields = [
            'id', 'user', 'name', 'description', 'layout', 'layout_display',
            'theme', 'theme_display', 'widgets', 'refresh_interval',
            'include_recommendations', 'export_formats', 'custom_styling',
            'is_default', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate_refresh_interval(self, value):
        """Ensure refresh interval is within reasonable bounds"""
        if value is not None and (value < 30 or value > 3600):  # 30 seconds to 1 hour
            raise serializers.ValidationError("Refresh interval must be between 30 and 3600 seconds")
        return value
    
    def validate_widgets(self, value):
        """Validate widgets configuration"""
        if value and not isinstance(value, list):
            raise serializers.ValidationError("Widgets must be a list")
        return value
    
    def validate_custom_styling(self, value):
        """Validate custom styling configuration"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Custom styling must be a dictionary")
        return value


class ReportTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for ReportTemplate model
    """
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    format_display = serializers.CharField(source='get_format_display', read_only=True)
    
    class Meta:
        model = ReportTemplate
        fields = [
            'id', 'name', 'description', 'report_type', 'report_type_display',
            'format', 'format_display', 'template_content', 'parameters',
            'scheduling', 'recipients', 'created_by', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def validate_template_content(self, value):
        """Validate template content"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Template content must be a dictionary")
        return value
    
    def validate_parameters(self, value):
        """Validate parameters configuration"""
        if value and not isinstance(value, list):
            raise serializers.ValidationError("Parameters must be a list")
        return value
    
    def validate_scheduling(self, value):
        """Validate scheduling configuration"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Scheduling must be a dictionary")
        return value
    
    def validate_recipients(self, value):
        """Validate recipients configuration"""
        if value and not isinstance(value, list):
            raise serializers.ValidationError("Recipients must be a list")
        return value


class StudentAnalyticsDashboardSerializer(serializers.Serializer):
    """
    Serializer for comprehensive student analytics dashboard
    """
    student = serializers.DictField()
    learning_analytics = LearningAnalyticsSerializer(many=True)
    performance_metrics = PerformanceMetricsSerializer(many=True)
    engagement_analytics = EngagementAnalyticsSerializer(many=True)
    recent_academic_records = serializers.ListField()
    summary_statistics = serializers.DictField()
    
    class Meta:
        fields = [
            'student', 'learning_analytics', 'performance_metrics',
            'engagement_analytics', 'recent_academic_records', 'summary_statistics'
        ]


class ClassAnalyticsSerializer(serializers.Serializer):
    """
    Serializer for class-level analytics
    """
    grade_level = serializers.CharField()
    total_students = serializers.IntegerField()
    learning_analytics = serializers.DictField()
    performance_metrics = serializers.DictField()
    engagement_analytics = serializers.DictField()
    subject_performance = serializers.ListField()
    generated_at = serializers.DateTimeField()
    
    class Meta:
        fields = [
            'grade_level', 'total_students', 'learning_analytics',
            'performance_metrics', 'engagement_analytics', 'subject_performance', 'generated_at'
        ]


class AnalyticsExportSerializer(serializers.Serializer):
    """
    Serializer for analytics export requests
    """
    format = serializers.ChoiceField(choices=['json', 'csv', 'xlsx'], default='json')
    filters = serializers.DictField(required=False, help_text="Filter criteria for export")
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


class AnalyticsInsightsSerializer(serializers.Serializer):
    """
    Serializer for analytics insights
    """
    insights = serializers.ListField()
    data_sources = serializers.ListField()
    generated_at = serializers.DateTimeField()
    
    class Meta:
        fields = ['insights', 'data_sources', 'generated_at']


class AnalyticsFilterSerializer(serializers.Serializer):
    """
    Serializer for analytics filtering
    """
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="List of student IDs to filter by"
    )
    date_from = serializers.DateField(required=False, help_text="Start date for filtering")
    date_to = serializers.DateField(required=False, help_text="End date for filtering")
    subjects = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of subjects to filter by"
    )
    grade_levels = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of grade levels to filter by"
    )
    performance_range = serializers.CharField(
        required=False,
        help_text="Performance range (e.g., '3.0-4.0')"
    )
    
    def validate_performance_range(self, value):
        """Validate performance range format"""
        if value:
            try:
                min_grade, max_grade = map(float, value.split('-'))
                if min_grade < 0 or max_grade > 4 or min_grade > max_grade:
                    raise ValueError("Invalid range")
            except (ValueError, TypeError):
                raise serializers.ValidationError("Performance range must be in format 'min-max' (e.g., '3.0-4.0')")
        return value