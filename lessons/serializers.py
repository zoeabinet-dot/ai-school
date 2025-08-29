from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Lesson, LessonPlan, LessonMaterial, LessonAssessment

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for Lesson model
    """
    subject_display = serializers.CharField(source='get_subject_display', read_only=True)
    lesson_type_display = serializers.CharField(source='get_lesson_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'subject', 'subject_display',
            'grade_level', 'lesson_type', 'lesson_type_display', 'difficulty',
            'difficulty_display', 'duration_minutes', 'learning_objectives',
            'prerequisites', 'materials_required', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LessonPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for LessonPlan model
    """
    lesson = LessonSerializer(read_only=True)
    
    class Meta:
        model = LessonPlan
        fields = [
            'id', 'lesson', 'plan_title', 'plan_description', 'learning_outcomes',
            'activities', 'time_allocation', 'assessment_criteria', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LessonMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for LessonMaterial model
    """
    lesson = LessonSerializer(read_only=True)
    
    class Meta:
        model = LessonMaterial
        fields = [
            'id', 'lesson', 'material_type', 'title', 'description',
            'file_path', 'url', 'content', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LessonAssessmentSerializer(serializers.ModelSerializer):
    """
    Serializer for LessonAssessment model
    """
    lesson = LessonSerializer(read_only=True)
    
    class Meta:
        model = LessonAssessment
        fields = [
            'id', 'lesson', 'assessment_type', 'title', 'description',
            'questions', 'scoring_criteria', 'time_limit', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
