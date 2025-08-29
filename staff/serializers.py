from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Staff, StaffProfile, StaffAssignment
from accounts.serializers import UserSerializer

User = get_user_model()


class StaffSerializer(serializers.ModelSerializer):
    """
    Serializer for Staff model
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='staff'),
        source='user',
        write_only=True
    )
    department_display = serializers.CharField(source='get_department_display', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Staff
        fields = [
            'id', 'user', 'user_id', 'employee_id', 'department', 'department_display',
            'role', 'role_display', 'hire_date', 'status', 'status_display',
            'qualifications', 'specializations', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StaffProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for StaffProfile model
    """
    staff = StaffSerializer(read_only=True)
    
    class Meta:
        model = StaffProfile
        fields = [
            'id', 'staff', 'assigned_grades', 'assigned_subjects',
            'teaching_experience', 'certifications', 'preferences',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StaffAssignmentSerializer(serializers.Serializer):
    """
    Serializer for StaffAssignment model
    """
    staff = StaffSerializer()
    assigned_grades = serializers.ListField()
    assigned_subjects = serializers.ListField()
    
    class Meta:
        fields = ['staff', 'assigned_grades', 'assigned_subjects']
