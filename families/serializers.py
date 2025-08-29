from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Family, FamilyMember, FamilyStudent
from accounts.serializers import UserSerializer

User = get_user_model()


class FamilySerializer(serializers.ModelSerializer):
    """
    Serializer for Family model
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='family'),
        source='user',
        write_only=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Family
        fields = [
            'id', 'user', 'user_id', 'family_name', 'primary_contact_name',
            'primary_contact_email', 'primary_contact_phone', 'address',
            'location', 'emergency_contact', 'status', 'status_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FamilyMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for FamilyMember model
    """
    family = FamilySerializer(read_only=True)
    relationship_display = serializers.CharField(source='get_relationship_display', read_only=True)
    
    class Meta:
        model = FamilyMember
        fields = [
            'id', 'family', 'name', 'relationship', 'relationship_display',
            'date_of_birth', 'contact_info', 'emergency_contact', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FamilyStudentSerializer(serializers.ModelSerializer):
    """
    Serializer for FamilyStudent model
    """
    family = FamilySerializer(read_only=True)
    student = serializers.DictField(read_only=True)
    
    class Meta:
        model = FamilyStudent
        fields = [
            'id', 'family', 'student', 'relationship', 'guardian_status',
            'contact_preferences', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
