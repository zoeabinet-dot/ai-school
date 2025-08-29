from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime, timedelta

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Student, AcademicRecord, StudentProject, LearningSession, StudentGoal
from .serializers import (
    StudentSerializer, AcademicRecordSerializer, StudentProjectSerializer,
    LearningSessionSerializer, StudentGoalSerializer
)
from accounts.models import User


class StudentListView(APIView):
    """
    List all students with filtering options
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or request.user.is_family):
            raise PermissionDenied("Insufficient permissions to view students")
        
        students = Student.objects.all()
        
        # Apply filters
        grade_level = request.query_params.get('grade_level')
        subject = request.query_params.get('subject')
        performance_level = request.query_params.get('performance_level')
        family_id = request.query_params.get('family_id')
        
        if grade_level:
            students = students.filter(grade_level=grade_level)
        if subject:
            students = students.filter(academic_records__subject__icontains=subject).distinct()
        if performance_level:
            students = students.filter(academic_records__overall_grade__gte=performance_level)
        if family_id and request.user.is_family:
            students = students.filter(family_id=family_id)
        
        # Role-based filtering
        if request.user.is_family:
            # Family can only see their own students
            students = students.filter(family=request.user)
        elif request.user.is_staff_member:
            # Staff can see students in their assigned classes
            students = students.filter(grade_level__in=request.user.staff_profile.assigned_grades)
        
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class StudentCreateView(APIView):
    """
    Create a new student
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create students")
        
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    """
    Get detailed information about a student
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        
        # Check permissions
        if not self.can_view_student(request.user, student):
            raise PermissionDenied("Insufficient permissions to view this student")
        
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def put(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        
        # Check permissions
        if not self.can_edit_student(request.user, student):
            raise PermissionDenied("Insufficient permissions to edit this student")
        
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            student = serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        
        # Check permissions
        if not (request.user.is_admin):
            raise PermissionDenied("Only administrators can delete students")
        
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def can_view_student(self, user, student):
        if user.is_admin or user.is_staff_member:
            return True
        elif user.is_family:
            return student.family == user
        elif user.is_student:
            return student.user == user
        return False
    
    def can_edit_student(self, user, student):
        if user.is_admin:
            return True
        elif user.is_staff_member:
            return student.grade_level in user.staff_profile.assigned_grades
        elif user.is_family:
            return student.family == user
        return False


class AcademicRecordListView(APIView):
    """
    List academic records for a student
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Check permissions
        if not self.can_view_student(request.user, student):
            raise PermissionDenied("Insufficient permissions to view this student's records")
        
        records = AcademicRecord.objects.filter(student=student)
        
        # Apply filters
        subject = request.query_params.get('subject')
        semester = request.query_params.get('semester')
        year = request.query_params.get('year')
        
        if subject:
            records = records.filter(subject__icontains=subject)
        if semester:
            records = records.filter(semester=semester)
        if year:
            records = records.filter(academic_year=year)
        
        serializer = AcademicRecordSerializer(records, many=True)
        return Response(serializer.data)


class AcademicRecordCreateView(APIView):
    """
    Create a new academic record
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create academic records")
        
        data = request.data.copy()
        data['student'] = student.id
        
        serializer = AcademicRecordSerializer(data=data)
        if serializer.is_valid():
            record = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentProjectListView(APIView):
    """
    List projects for a student
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Check permissions
        if not self.can_view_student(request.user, student):
            raise PermissionDenied("Insufficient permissions to view this student's projects")
        
        projects = StudentProject.objects.filter(student=student)
        
        # Apply filters
        project_type = request.query_params.get('project_type')
        subject = request.query_params.get('subject')
        status_filter = request.query_params.get('status')
        
        if project_type:
            projects = projects.filter(project_type=project_type)
        if subject:
            projects = projects.filter(subject__icontains=subject)
        if status_filter:
            projects = projects.filter(status=status_filter)
        
        serializer = StudentProjectSerializer(projects, many=True)
        return Response(serializer.data)


class StudentProjectCreateView(APIView):
    """
    Create a new student project
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def post(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or 
                (request.user.is_student and student.user == request.user)):
            raise PermissionDenied("Insufficient permissions to create projects")
        
        data = request.data.copy()
        data['student'] = student.id
        
        serializer = StudentProjectSerializer(data=data)
        if serializer.is_valid():
            project = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LearningSessionListView(APIView):
    """
    List learning sessions for a student
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Check permissions
        if not self.can_view_student(request.user, student):
            raise PermissionDenied("Insufficient permissions to view this student's sessions")
        
        sessions = LearningSession.objects.filter(student=student)
        
        # Apply filters
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        session_type = request.query_params.get('session_type')
        
        if date_from:
            sessions = sessions.filter(start_time__gte=date_from)
        if date_to:
            sessions = sessions.filter(end_time__lte=date_to)
        if session_type:
            sessions = sessions.filter(session_type=session_type)
        
        serializer = LearningSessionSerializer(sessions, many=True)
        return Response(serializer.data)


class LearningSessionCreateView(APIView):
    """
    Create a new learning session
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or 
                (request.user.is_student and student.user == request.user)):
            raise PermissionDenied("Insufficient permissions to create sessions")
        
        data = request.data.copy()
        data['student'] = student.id
        data['start_time'] = timezone.now()
        
        serializer = LearningSessionSerializer(data=data)
        if serializer.is_valid():
            session = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LearningSessionEndView(APIView):
    """
    End a learning session
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, session_id):
        session = get_object_or_404(LearningSession, pk=session_id)
        
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or 
                (request.user.is_student and session.student.user == request.user)):
            raise PermissionDenied("Insufficient permissions to end this session")
        
        session.end_time = timezone.now()
        session.duration = (session.end_time - session.start_time).total_seconds() / 60  # in minutes
        session.save()
        
        serializer = LearningSessionSerializer(session)
        return Response(serializer.data)


class StudentGoalListView(APIView):
    """
    List goals for a student
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Check permissions
        if not self.can_view_student(request.user, student):
            raise PermissionDenied("Insufficient permissions to view this student's goals")
        
        goals = StudentGoal.objects.filter(student=student)
        
        # Apply filters
        goal_type = request.query_params.get('goal_type')
        status_filter = request.query_params.get('status')
        priority = request.query_params.get('priority')
        
        if goal_type:
            goals = goals.filter(goal_type=goal_type)
        if status_filter:
            goals = goals.filter(status=status_filter)
        if priority:
            goals = goals.filter(priority=priority)
        
        serializer = StudentGoalSerializer(goals, many=True)
        return Response(serializer.data)


class StudentGoalCreateView(APIView):
    """
    Create a new student goal
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or 
                (request.user.is_family and student.family == request.user)):
            raise PermissionDenied("Insufficient permissions to create goals")
        
        data = request.data.copy()
        data['student'] = student.id
        
        serializer = StudentGoalSerializer(data=data)
        if serializer.is_valid():
            goal = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentGoalUpdateView(APIView):
    """
    Update a student goal
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, goal_id):
        goal = get_object_or_404(StudentGoal, pk=goal_id)
        
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or 
                (request.user.is_family and goal.student.family == request.user)):
            raise PermissionDenied("Insufficient permissions to update this goal")
        
        serializer = StudentGoalSerializer(goal, data=request.data, partial=True)
        if serializer.is_valid():
            goal = serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDashboardView(APIView):
    """
    Get comprehensive student dashboard data
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Check permissions
        if not self.can_view_student(request.user, student):
            raise PermissionDenied("Insufficient permissions to view this student's dashboard")
        
        # Get recent academic records
        recent_records = AcademicRecord.objects.filter(student=student).order_by('-academic_year', '-semester')[:5]
        
        # Get active projects
        active_projects = StudentProject.objects.filter(student=student, status='in_progress')
        
        # Get recent learning sessions
        recent_sessions = LearningSession.objects.filter(student=student).order_by('-start_time')[:10]
        
        # Get active goals
        active_goals = StudentGoal.objects.filter(student=student, status='active')
        
        # Calculate performance metrics
        total_sessions = LearningSession.objects.filter(student=student).count()
        total_duration = sum([s.duration or 0 for s in LearningSession.objects.filter(student=student)])
        from django.db import models
        avg_grade = AcademicRecord.objects.filter(student=student).aggregate(
            avg=models.Avg('overall_grade')
        )['avg'] or 0
        
        dashboard_data = {
            'student': StudentSerializer(student).data,
            'recent_records': AcademicRecordSerializer(recent_records, many=True).data,
            'active_projects': StudentProjectSerializer(active_projects, many=True).data,
            'recent_sessions': LearningSessionSerializer(recent_sessions, many=True).data,
            'active_goals': StudentGoalSerializer(active_goals, many=True).data,
            'metrics': {
                'total_sessions': total_sessions,
                'total_duration_minutes': total_duration,
                'average_grade': round(avg_grade, 2),
                'projects_in_progress': active_projects.count(),
                'active_goals': active_goals.count()
            }
        }
        
        return Response(dashboard_data)


class StudentSearchView(APIView):
    """
    Search students with advanced filtering
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Insufficient permissions to search students")
        
        query = request.query_params.get('q', '')
        grade_level = request.query_params.get('grade_level')
        subject = request.query_params.get('subject')
        performance_range = request.query_params.get('performance_range')
        
        students = Student.objects.all()
        
        if query:
            students = students.filter(
                models.Q(user__first_name__icontains=query) |
                models.Q(user__last_name__icontains=query) |
                models.Q(user__username__icontains=query) |
                models.Q(student_id__icontains=query)
            )
        
        if grade_level:
            students = students.filter(grade_level=grade_level)
        
        if subject:
            students = students.filter(academic_records__subject__icontains=subject).distinct()
        
        if performance_range:
            min_grade, max_grade = map(float, performance_range.split('-'))
            students = students.filter(
                academic_records__overall_grade__gte=min_grade,
                academic_records__overall_grade__lte=max_grade
            )
        
        # Role-based filtering
        if request.user.is_staff_member:
            students = students.filter(grade_level__in=request.user.staff_profile.assigned_grades)
        
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


# Legacy view for backward compatibility
def student_list(request):
    return JsonResponse({'message': 'Use API endpoints for student data'})
