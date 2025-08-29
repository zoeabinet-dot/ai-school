from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import models
import json
from datetime import datetime, timedelta

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Lesson, LessonPlan, LessonMaterial, LessonAssessment
from .serializers import (
    LessonSerializer, LessonPlanSerializer, LessonMaterialSerializer, LessonAssessmentSerializer
)
from students.models import Student
from accounts.models import User


class LessonListView(APIView):
    """
    List all lessons with filtering options
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or request.user.is_student):
            raise PermissionDenied("Insufficient permissions to view lessons")
        
        lessons = Lesson.objects.all()
        
        # Apply filters
        subject = request.query_params.get('subject')
        grade_level = request.query_params.get('grade_level')
        lesson_type = request.query_params.get('lesson_type')
        
        if subject:
            lessons = lessons.filter(subject__icontains=subject)
        if grade_level:
            lessons = lessons.filter(grade_level=grade_level)
        if lesson_type:
            lessons = lessons.filter(lesson_type=lesson_type)
        
        # Role-based filtering
        if request.user.is_student:
            lessons = lessons.filter(grade_level=request.user.student_profile.grade_level)
        elif request.user.is_staff_member:
            lessons = lessons.filter(grade_level__in=request.user.staff_profile.assigned_grades)
        
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class LessonCreateView(APIView):
    """
    Create a new lesson
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create lessons")
        
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            lesson = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDetailView(APIView):
    """
    Get detailed information about a lesson
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        
        # Check permissions
        if not self.can_view_lesson(request.user, lesson):
            raise PermissionDenied("Insufficient permissions to view this lesson")
        
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)
    
    def can_view_lesson(self, user, lesson):
        if user.is_admin or user.is_staff_member:
            return True
        elif user.is_student:
            return lesson.grade_level == user.student_profile.grade_level
        return False


class LessonPlanListView(APIView):
    """
    List lesson plans for a lesson
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        
        # Check permissions
        if not self.can_view_lesson(request.user, lesson):
            raise PermissionDenied("Insufficient permissions to view this lesson's plans")
        
        plans = LessonPlan.objects.filter(lesson=lesson)
        serializer = LessonPlanSerializer(plans, many=True)
        return Response(serializer.data)


class LessonMaterialListView(APIView):
    """
    List materials for a lesson
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        
        # Check permissions
        if not self.can_view_lesson(request.user, lesson):
            raise PermissionDenied("Insufficient permissions to view this lesson's materials")
        
        materials = LessonMaterial.objects.filter(lesson=lesson)
        serializer = LessonMaterialSerializer(materials, many=True)
        return Response(serializer.data)


class LessonAssessmentListView(APIView):
    """
    List assessments for a lesson
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        
        # Check permissions
        if not self.can_view_lesson(request.user, lesson):
            raise PermissionDenied("Insufficient permissions to view this lesson's assessments")
        
        assessments = LessonAssessment.objects.filter(lesson=lesson)
        serializer = LessonAssessmentSerializer(assessments, many=True)
        return Response(serializer.data)


# Legacy view for backward compatibility
def lesson_list(request):
    return JsonResponse({'message': 'Use API endpoints for lesson data'})
