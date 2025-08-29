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

from .models import Family, FamilyMember, FamilyStudent
from .serializers import (
    FamilySerializer, FamilyMemberSerializer, FamilyStudentSerializer
)
from students.models import Student, AcademicRecord, LearningSession
from accounts.models import User


class FamilyListView(APIView):
    """
    List families with filtering options
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can view all families")
        
        families = Family.objects.all()
        
        # Apply filters
        family_name = request.query_params.get('family_name')
        location = request.query_params.get('location')
        status_filter = request.query_params.get('status')
        
        if family_name:
            families = families.filter(family_name__icontains=family_name)
        if location:
            families = families.filter(location__icontains=location)
        if status_filter:
            families = families.filter(status=status_filter)
        
        serializer = FamilySerializer(families, many=True)
        return Response(serializer.data)


class FamilyCreateView(APIView):
    """
    Create a new family
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create families")
        
        serializer = FamilySerializer(data=request.data)
        if serializer.is_valid():
            family = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FamilyDetailView(APIView):
    """
    Get detailed information about a family
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        family = get_object_or_404(Family, pk=pk)
        
        # Check permissions
        if not self.can_view_family(request.user, family):
            raise PermissionDenied("Insufficient permissions to view this family")
        
        serializer = FamilySerializer(family)
        return Response(serializer.data)
    
    def can_view_family(self, user, family):
        if user.is_admin or user.is_staff_member:
            return True
        elif user.is_family:
            return family.user == user
        return False


class FamilyMemberListView(APIView):
    """
    List family members for a family
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, family_id):
        family = get_object_or_404(Family, pk=family_id)
        
        # Check permissions
        if not self.can_view_family(request.user, family):
            raise PermissionDenied("Insufficient permissions to view this family's members")
        
        members = FamilyMember.objects.filter(family=family)
        serializer = FamilyMemberSerializer(members, many=True)
        return Response(serializer.data)


class FamilyMemberCreateView(APIView):
    """
    Create a new family member
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, family_id):
        family = get_object_or_404(Family, pk=family_id)
        
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or 
                (request.user.is_family and family.user == request.user)):
            raise PermissionDenied("Insufficient permissions to create family members")
        
        data = request.data.copy()
        data['family'] = family.id
        
        serializer = FamilyMemberSerializer(data=data)
        if serializer.is_valid():
            member = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FamilyStudentListView(APIView):
    """
    List students associated with a family
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, family_id):
        family = get_object_or_404(Family, pk=family_id)
        
        # Check permissions
        if not self.can_view_family(request.user, family):
            raise PermissionDenied("Insufficient permissions to view this family's students")
        
        students = FamilyStudent.objects.filter(family=family)
        serializer = FamilyStudentSerializer(students, many=True)
        return Response(serializer.data)


class FamilyStudentCreateView(APIView):
    """
    Associate a student with a family
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, family_id):
        family = get_object_or_404(Family, pk=family_id)
        
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can associate students with families")
        
        data = request.data.copy()
        data['family'] = family.id
        
        serializer = FamilyStudentSerializer(data=data)
        if serializer.is_valid():
            family_student = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FamilyDashboardView(APIView):
    """
    Get comprehensive family dashboard data
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, family_id):
        family = get_object_or_404(Family, pk=family_id)
        
        # Check permissions
        if not self.can_view_family(request.user, family):
            raise PermissionDenied("Insufficient permissions to view this family's dashboard")
        
        # Get family members
        family_members = FamilyMember.objects.filter(family=family)
        
        # Get associated students
        family_students = FamilyStudent.objects.filter(family=family)
        student_ids = [fs.student.id for fs in family_students]
        
        # Get student academic records
        academic_records = AcademicRecord.objects.filter(student_id__in=student_ids).order_by('-academic_year', '-semester')[:20]
        
        # Get learning sessions
        learning_sessions = LearningSession.objects.filter(student_id__in=student_ids).order_by('-start_time')[:30]
        
        # Calculate family statistics
        total_students = family_students.count()
        total_members = family_members.count()
        
        # Calculate academic performance
        if academic_records.exists():
            avg_grade = academic_records.aggregate(avg=models.Avg('overall_grade'))['avg'] or 0
            total_attendance = academic_records.aggregate(avg=models.Avg('attendance_percentage'))['avg'] or 0
        else:
            avg_grade = 0
            total_attendance = 0
        
        # Calculate learning engagement
        if learning_sessions.exists():
            total_learning_time = sum([s.duration or 0 for s in learning_sessions])
            avg_session_duration = total_learning_time / learning_sessions.count() if learning_sessions.count() > 0 else 0
        else:
            total_learning_time = 0
            avg_session_duration = 0
        
        dashboard_data = {
            'family': FamilySerializer(family).data,
            'family_members': FamilyMemberSerializer(family_members, many=True).data,
            'family_students': FamilyStudentSerializer(family_students, many=True).data,
            'recent_academic_records': [
                {
                    'student_name': record.student.user.get_full_name(),
                    'subject': record.subject,
                    'semester': record.semester,
                    'academic_year': record.academic_year,
                    'overall_grade': record.overall_grade,
                    'attendance_percentage': record.attendance_percentage
                }
                for record in academic_records
            ],
            'recent_learning_sessions': [
                {
                    'student_name': session.student.user.get_full_name(),
                    'session_type': session.session_type,
                    'start_time': session.start_time,
                    'duration': session.duration,
                    'engagement_score': session.engagement_score
                }
                for session in learning_sessions
            ],
            'family_statistics': {
                'total_students': total_students,
                'total_members': total_members,
                'average_grade': round(avg_grade, 2),
                'average_attendance': round(total_attendance, 2),
                'total_learning_time_minutes': round(total_learning_time, 2),
                'average_session_duration_minutes': round(avg_session_duration, 2),
                'total_academic_records': academic_records.count(),
                'total_learning_sessions': learning_sessions.count()
            }
        }
        
        return Response(dashboard_data)


class FamilySearchView(APIView):
    """
    Search families with advanced filtering
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can search families")
        
        query = request.query_params.get('q', '')
        location = request.query_params.get('location')
        student_count_min = request.query_params.get('student_count_min')
        student_count_max = request.query_params.get('student_count_max')
        
        families = Family.objects.all()
        
        if query:
            families = families.filter(
                models.Q(family_name__icontains=query) |
                models.Q(primary_contact_name__icontains=query) |
                models.Q(primary_contact_email__icontains=query)
            )
        
        if location:
            families = families.filter(location__icontains=location)
        
        if student_count_min:
            families = families.annotate(
                student_count=models.Count('family_students')
            ).filter(student_count__gte=int(student_count_min))
        
        if student_count_max:
            families = families.annotate(
                student_count=models.Count('family_students')
            ).filter(student_count__lte=int(student_count_max))
        
        serializer = FamilySerializer(families, many=True)
        return Response(serializer.data)


# Legacy view for backward compatibility
def family_list(request):
    return JsonResponse({'message': 'Use API endpoints for family data'})
