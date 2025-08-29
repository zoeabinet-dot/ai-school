from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Student, AcademicRecord, StudentProject, LearningSession, StudentGoal
from accounts.serializers import UserSerializer, UserProfileSerializer

User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model with nested user data
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='student'),
        source='user',
        write_only=True
    )
    family_name = serializers.CharField(source='family.get_full_name', read_only=True)
    grade_level_display = serializers.CharField(source='get_grade_level_display', read_only=True)
    academic_status_display = serializers.CharField(source='get_academic_status_display', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'user_id', 'student_id', 'grade_level', 'grade_level_display',
            'academic_status', 'academic_status_display', 'enrollment_date', 'graduation_date',
            'family', 'family_name', 'emergency_contact', 'medical_info', 'special_needs',
            'learning_preferences', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_student_id(self, value):
        """Ensure student_id is unique"""
        if Student.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("Student ID must be unique")
        return value
    
    def validate_enrollment_date(self, value):
        """Ensure enrollment date is not in the future"""
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Enrollment date cannot be in the future")
        return value
    
    def validate_graduation_date(self, value):
        """Ensure graduation date is after enrollment date"""
        enrollment_date = self.initial_data.get('enrollment_date')
        if value and enrollment_date and value <= enrollment_date:
            raise serializers.ValidationError("Graduation date must be after enrollment date")
        return value


class AcademicRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for AcademicRecord model
    """
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_display = serializers.CharField(source='get_subject_display', read_only=True)
    semester_display = serializers.CharField(source='get_semester_display', read_only=True)
    
    class Meta:
        model = AcademicRecord
        fields = [
            'id', 'student', 'student_name', 'subject', 'subject_display', 'semester',
            'semester_display', 'academic_year', 'overall_grade', 'attendance_percentage',
            'participation_score', 'homework_completion', 'test_scores', 'project_scores',
            'teacher_comments', 'student_comments', 'parent_comments', 'created_at', 'updated_at'
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
    
    def validate_participation_score(self, value):
        """Ensure participation score is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Participation score must be between 0 and 100")
        return value


class StudentProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentProject model
    """
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    project_type_display = serializers.CharField(source='get_project_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    subject_display = serializers.CharField(source='get_subject_display', read_only=True)
    
    class Meta:
        model = StudentProject
        fields = [
            'id', 'student', 'student_name', 'title', 'description', 'project_type',
            'project_type_display', 'subject', 'subject_display', 'status', 'status_display',
            'start_date', 'due_date', 'completion_date', 'grade', 'feedback',
            'thumbnail', 'project_file', 'github_url', 'demo_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_due_date(self, value):
        """Ensure due date is not in the past"""
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value
    
    def validate_completion_date(self, value):
        """Ensure completion date is not before start date"""
        start_date = self.initial_data.get('start_date')
        if value and start_date and value < start_date:
            raise serializers.ValidationError("Completion date cannot be before start date")
        return value
    
    def validate_grade(self, value):
        """Ensure grade is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Grade must be between 0 and 100")
        return value


class LearningSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for LearningSession model
    """
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    session_type_display = serializers.CharField(source='get_session_type_display', read_only=True)
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningSession
        fields = [
            'id', 'student', 'student_name', 'session_type', 'session_type_display',
            'start_time', 'end_time', 'duration', 'duration_formatted', 'subject',
            'lesson_topic', 'engagement_score', 'completion_rate', 'notes',
            'ai_assistance_used', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
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


class StudentGoalSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentGoal model
    """
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    goal_type_display = serializers.CharField(source='get_goal_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentGoal
        fields = [
            'id', 'student', 'student_name', 'title', 'description', 'goal_type',
            'goal_type_display', 'target_date', 'status', 'status_display', 'priority',
            'priority_display', 'progress_percentage', 'milestones', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_progress_percentage(self, obj):
        """Calculate progress percentage based on milestones"""
        if obj.milestones:
            completed = sum(1 for milestone in obj.milestones if milestone.get('completed', False))
            total = len(obj.milestones)
            if total > 0:
                return round((completed / total) * 100, 1)
        return 0.0
    
    def validate_target_date(self, value):
        """Ensure target date is not in the past"""
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Target date cannot be in the past")
        return value


class StudentDashboardSerializer(serializers.Serializer):
    """
    Serializer for comprehensive student dashboard data
    """
    student = StudentSerializer()
    recent_records = AcademicRecordSerializer(many=True)
    active_projects = StudentProjectSerializer(many=True)
    recent_sessions = LearningSessionSerializer(many=True)
    active_goals = StudentGoalSerializer(many=True)
    metrics = serializers.DictField()
    
    class Meta:
        fields = ['student', 'recent_records', 'active_projects', 'recent_sessions', 'active_goals', 'metrics']


class StudentSearchSerializer(serializers.Serializer):
    """
    Serializer for student search parameters
    """
    q = serializers.CharField(required=False, help_text="Search query for name or student ID")
    grade_level = serializers.CharField(required=False, help_text="Filter by grade level")
    subject = serializers.CharField(required=False, help_text="Filter by subject")
    performance_range = serializers.CharField(required=False, help_text="Filter by performance range (e.g., '3.0-4.0')")
    
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


class StudentBulkCreateSerializer(serializers.Serializer):
    """
    Serializer for bulk student creation
    """
    students = StudentSerializer(many=True)
    
    def create(self, validated_data):
        students_data = validated_data['students']
        created_students = []
        
        for student_data in students_data:
            student = Student.objects.create(**student_data)
            created_students.append(student)
        
        return {'students': created_students}


class StudentExportSerializer(serializers.Serializer):
    """
    Serializer for student data export
    """
    format = serializers.ChoiceField(choices=['csv', 'json', 'xlsx'], default='csv')
    include_fields = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of fields to include in export"
    )
    filters = serializers.DictField(required=False, help_text="Filter criteria for export")
    
    def validate_format(self, value):
        """Validate export format"""
        if value not in ['csv', 'json', 'xlsx']:
            raise serializers.ValidationError("Unsupported export format")
        return value


class StudentPerformanceReportSerializer(serializers.Serializer):
    """
    Serializer for student performance reports
    """
    student = StudentSerializer()
    academic_summary = serializers.DictField()
    subject_performance = serializers.ListField()
    attendance_summary = serializers.DictField()
    project_summary = serializers.DictField()
    goal_progress = serializers.ListField()
    recommendations = serializers.ListField()
    
    class Meta:
        fields = [
            'student', 'academic_summary', 'subject_performance', 'attendance_summary',
            'project_summary', 'goal_progress', 'recommendations'
        ]