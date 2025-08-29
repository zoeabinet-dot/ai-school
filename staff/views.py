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

from .models import Staff, StaffProfile, StaffAssignment
from .serializers import StaffSerializer, StaffProfileSerializer, StaffAssignmentSerializer
from students.models import Student, AcademicRecord
from accounts.models import User


class StaffListView(APIView):
    """
    List all staff members with filtering options
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Insufficient permissions to view staff")
        
        staff = Staff.objects.all()
        
        # Apply filters
        department = request.query_params.get('department')
        role = request.query_params.get('role')
        status_filter = request.query_params.get('status')
        
        if department:
            staff = staff.filter(department__icontains=department)
        if role:
            staff = staff.filter(role=role)
        if status_filter:
            staff = staff.filter(status=status_filter)
        
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)


class StaffCreateView(APIView):
    """
    Create a new staff member
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not request.user.is_admin:
            raise PermissionDenied("Only administrators can create staff members")
        
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            staff = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffDetailView(APIView):
    """
    Get detailed information about a staff member
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        staff = get_object_or_404(Staff, pk=pk)
        
        # Check permissions
        if not (request.user.is_admin or request.user == staff.user):
            raise PermissionDenied("Insufficient permissions to view this staff member")
        
        serializer = StaffSerializer(staff)
        return Response(serializer.data)


class StaffDashboardView(APIView):
    """
    Get comprehensive staff dashboard data
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, staff_id):
        staff = get_object_or_404(Staff, pk=staff_id)
        
        # Check permissions
        if not (request.user.is_admin or request.user == staff.user):
            raise PermissionDenied("Insufficient permissions to view this staff dashboard")
        
        # Get assigned students
        assigned_students = Student.objects.filter(grade_level__in=staff.profile.assigned_grades)
        
        # Get recent academic records for assigned students
        recent_records = AcademicRecord.objects.filter(
            student__in=assigned_students
        ).order_by('-academic_year', '-semester')[:20]
        
        # Calculate statistics
        total_students = assigned_students.count()
        avg_grade = recent_records.aggregate(avg=models.Avg('overall_grade'))['avg'] or 0
        
        dashboard_data = {
            'staff': StaffSerializer(staff).data,
            'assigned_students_count': total_students,
            'recent_academic_records': [
                {
                    'student_name': record.student.user.get_full_name(),
                    'subject': record.subject,
                    'semester': record.semester,
                    'academic_year': record.academic_year,
                    'overall_grade': record.overall_grade
                }
                for record in recent_records
            ],
            'statistics': {
                'total_assigned_students': total_students,
                'average_grade': round(avg_grade, 2),
                'total_academic_records': recent_records.count()
            }
        }
        
        return Response(dashboard_data)


# Legacy view for backward compatibility
def staff_list(request):
    return JsonResponse({'message': 'Use API endpoints for staff data'})
