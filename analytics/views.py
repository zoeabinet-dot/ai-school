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

from .models import (
    LearningAnalytics, PerformanceMetrics, EngagementAnalytics,
    DashboardConfiguration, ReportTemplate
)
from .serializers import (
    LearningAnalyticsSerializer, PerformanceMetricsSerializer, EngagementAnalyticsSerializer,
    DashboardConfigurationSerializer, ReportTemplateSerializer
)
from students.models import Student, AcademicRecord, LearningSession
from accounts.models import User


class LearningAnalyticsListView(APIView):
    """
    List learning analytics with filtering options
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or request.user.is_family):
            raise PermissionDenied("Insufficient permissions to view learning analytics")
        
        analytics = LearningAnalytics.objects.all()
        
        # Apply filters
        student_id = request.query_params.get('student_id')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        subject = request.query_params.get('subject')
        
        if student_id:
            analytics = analytics.filter(student_id=student_id)
        if date_from:
            analytics = analytics.filter(date__gte=date_from)
        if date_to:
            analytics = analytics.filter(date__lte=date_to)
        if subject:
            analytics = analytics.filter(subject__icontains=subject)
        
        # Role-based filtering
        if request.user.is_family:
            # Family can only see their own students' analytics
            student_ids = request.user.family_students.values_list('id', flat=True)
            analytics = analytics.filter(student_id__in=student_ids)
        elif request.user.is_staff_member:
            # Staff can see analytics for students in their assigned classes
            assigned_grades = request.user.staff_profile.assigned_grades
            analytics = analytics.filter(student__grade_level__in=assigned_grades)
        
        serializer = LearningAnalyticsSerializer(analytics, many=True)
        return Response(serializer.data)


class LearningAnalyticsCreateView(APIView):
    """
    Create new learning analytics
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create learning analytics")
        
        serializer = LearningAnalyticsSerializer(data=request.data)
        if serializer.is_valid():
            analytics = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LearningAnalyticsDetailView(APIView):
    """
    Get detailed learning analytics information
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        analytics = get_object_or_404(LearningAnalytics, pk=pk)
        
        # Check permissions
        if not self.can_view_analytics(request.user, analytics):
            raise PermissionDenied("Insufficient permissions to view this analytics")
        
        serializer = LearningAnalyticsSerializer(analytics)
        return Response(serializer.data)
    
    def can_view_analytics(self, user, analytics):
        if user.is_admin or user.is_staff_member:
            return True
        elif user.is_family:
            return analytics.student.family == user
        elif user.is_student:
            return analytics.student.user == user
        return False


class PerformanceMetricsListView(APIView):
    """
    List performance metrics with filtering options
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or request.user.is_family):
            raise PermissionDenied("Insufficient permissions to view performance metrics")
        
        metrics = PerformanceMetrics.objects.all()
        
        # Apply filters
        student_id = request.query_params.get('student_id')
        period_type = request.query_params.get('period_type')
        period_start = request.query_params.get('period_start')
        period_end = request.query_params.get('period_end')
        
        if student_id:
            metrics = metrics.filter(student_id=student_id)
        if period_type:
            metrics = metrics.filter(period_type=period_type)
        if period_start:
            metrics = metrics.filter(period_start__gte=period_start)
        if period_end:
            metrics = metrics.filter(period_end__lte=period_end)
        
        # Role-based filtering
        if request.user.is_family:
            student_ids = request.user.family_students.values_list('id', flat=True)
            metrics = metrics.filter(student_id__in=student_ids)
        elif request.user.is_staff_member:
            assigned_grades = request.user.staff_profile.assigned_grades
            metrics = metrics.filter(student__grade_level__in=assigned_grades)
        
        serializer = PerformanceMetricsSerializer(metrics, many=True)
        return Response(serializer.data)


class PerformanceMetricsCreateView(APIView):
    """
    Create new performance metrics
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create performance metrics")
        
        serializer = PerformanceMetricsSerializer(data=request.data)
        if serializer.is_valid():
            metrics = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EngagementAnalyticsListView(APIView):
    """
    List engagement analytics with filtering options
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or request.user.is_family):
            raise PermissionDenied("Insufficient permissions to view engagement analytics")
        
        analytics = EngagementAnalytics.objects.all()
        
        # Apply filters
        student_id = request.query_params.get('student_id')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        engagement_level = request.query_params.get('engagement_level')
        
        if student_id:
            analytics = analytics.filter(student_id=student_id)
        if date_from:
            analytics = analytics.filter(date__gte=date_from)
        if date_to:
            analytics = analytics.filter(date__lte=date_to)
        if engagement_level:
            analytics = analytics.filter(engagement_level=engagement_level)
        
        # Role-based filtering
        if request.user.is_family:
            student_ids = request.user.family_students.values_list('id', flat=True)
            analytics = analytics.filter(student_id__in=student_ids)
        elif request.user.is_staff_member:
            assigned_grades = request.user.staff_profile.assigned_grades
            analytics = analytics.filter(student__grade_level__in=assigned_grades)
        
        serializer = EngagementAnalyticsSerializer(analytics, many=True)
        return Response(serializer.data)


class DashboardConfigurationListView(APIView):
    """
    List dashboard configurations for users
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Users can only see their own dashboard configurations
        configs = DashboardConfiguration.objects.filter(user=request.user)
        serializer = DashboardConfigurationSerializer(configs, many=True)
        return Response(serializer.data)


class DashboardConfigurationCreateView(APIView):
    """
    Create new dashboard configuration
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        
        serializer = DashboardConfigurationSerializer(data=data)
        if serializer.is_valid():
            config = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DashboardConfigurationUpdateView(APIView):
    """
    Update dashboard configuration
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        config = get_object_or_404(DashboardConfiguration, pk=pk, user=request.user)
        
        serializer = DashboardConfigurationSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            config = serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportTemplateListView(APIView):
    """
    List report templates
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can view report templates")
        
        templates = ReportTemplate.objects.all()
        serializer = ReportTemplateSerializer(templates, many=True)
        return Response(serializer.data)


class ReportTemplateCreateView(APIView):
    """
    Create new report template
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create report templates")
        
        serializer = ReportTemplateSerializer(data=request.data)
        if serializer.is_valid():
            template = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentAnalyticsDashboardView(APIView):
    """
    Get comprehensive analytics dashboard for a specific student
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Check permissions
        if not self.can_view_student_analytics(request.user, student):
            raise PermissionDenied("Insufficient permissions to view this student's analytics")
        
        # Get learning analytics
        learning_analytics = LearningAnalytics.objects.filter(student=student).order_by('-date')[:30]
        
        # Get performance metrics
        performance_metrics = PerformanceMetrics.objects.filter(student=student).order_by('-period_end')[:12]
        
        # Get engagement analytics
        engagement_analytics = EngagementAnalytics.objects.filter(student=student).order_by('-date')[:30]
        
        # Calculate summary statistics
        total_learning_hours = sum([a.total_learning_time for a in learning_analytics])
        avg_engagement_score = engagement_analytics.aggregate(
            avg=models.Avg('total_engagement_score')
        )['avg'] or 0
        
        # Get recent academic performance
        recent_academic_records = AcademicRecord.objects.filter(student=student).order_by('-academic_year', '-semester')[:10]
        
        dashboard_data = {
            'student': {
                'id': student.id,
                'name': student.user.get_full_name(),
                'grade_level': student.grade_level,
                'academic_status': student.academic_status
            },
            'learning_analytics': LearningAnalyticsSerializer(learning_analytics, many=True).data,
            'performance_metrics': PerformanceMetricsSerializer(performance_metrics, many=True).data,
            'engagement_analytics': EngagementAnalyticsSerializer(engagement_analytics, many=True).data,
            'recent_academic_records': [
                {
                    'subject': record.subject,
                    'semester': record.semester,
                    'academic_year': record.academic_year,
                    'overall_grade': record.overall_grade,
                    'attendance_percentage': record.attendance_percentage
                }
                for record in recent_academic_records
            ],
            'summary_statistics': {
                'total_learning_hours': round(total_learning_hours, 2),
                'average_engagement_score': round(avg_engagement_score, 2),
                'total_analytics_records': learning_analytics.count() + performance_metrics.count() + engagement_analytics.count(),
                'data_coverage_days': learning_analytics.count()
            }
        }
        
        return Response(dashboard_data)
    
    def can_view_student_analytics(self, user, student):
        if user.is_admin or user.is_staff_member:
            return True
        elif user.is_family:
            return student.family == user
        elif user.is_student:
            return student.user == user
        return False


class ClassAnalyticsView(APIView):
    """
    Get analytics for an entire class/grade level
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, grade_level):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can view class analytics")
        
        # Get all students in the grade level
        students = Student.objects.filter(grade_level=grade_level)
        
        # Get aggregated analytics
        class_learning_analytics = LearningAnalytics.objects.filter(
            student__grade_level=grade_level
        ).aggregate(
            total_students=models.Count('student', distinct=True),
            avg_learning_time=models.Avg('total_learning_time'),
            avg_subject_mastery=models.Avg('subject_mastery_level'),
            total_sessions=models.Sum('total_sessions')
        )
        
        class_performance_metrics = PerformanceMetrics.objects.filter(
            student__grade_level=grade_level
        ).aggregate(
            avg_overall_grade=models.Avg('overall_grade'),
            avg_attendance=models.Avg('attendance_percentage'),
            avg_improvement=models.Avg('improvement_rate')
        )
        
        class_engagement_analytics = EngagementAnalytics.objects.filter(
            student__grade_level=grade_level
        ).aggregate(
            avg_engagement_score=models.Avg('total_engagement_score'),
            avg_participation=models.Avg('participation_rate'),
            avg_retention=models.Avg('retention_rate')
        )
        
        # Get subject-wise performance
        subject_performance = AcademicRecord.objects.filter(
            student__grade_level=grade_level
        ).values('subject').annotate(
            avg_grade=models.Avg('overall_grade'),
            total_students=models.Count('student', distinct=True)
        ).order_by('-avg_grade')
        
        class_data = {
            'grade_level': grade_level,
            'total_students': students.count(),
            'learning_analytics': class_learning_analytics,
            'performance_metrics': class_performance_metrics,
            'engagement_analytics': class_engagement_analytics,
            'subject_performance': list(subject_performance),
            'generated_at': timezone.now()
        }
        
        return Response(class_data)


class AnalyticsExportView(APIView):
    """
    Export analytics data in various formats
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can export analytics")
        
        export_format = request.data.get('format', 'json')
        filters = request.data.get('filters', {})
        include_fields = request.data.get('include_fields', [])
        
        # Apply filters to get data
        analytics_data = self.get_filtered_analytics(filters)
        
        # Export based on format
        if export_format == 'json':
            return Response(analytics_data)
        elif export_format == 'csv':
            # For CSV export, you would typically use a library like pandas
            return Response({'message': 'CSV export not yet implemented'})
        else:
            return Response({'error': 'Unsupported export format'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_filtered_analytics(self, filters):
        """Get analytics data based on filters"""
        # This is a simplified implementation
        # In a real application, you would implement proper filtering logic
        return {
            'message': 'Analytics export functionality',
            'filters_applied': filters,
            'timestamp': timezone.now()
        }


class AnalyticsInsightsView(APIView):
    """
    Get AI-generated insights from analytics data
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can view analytics insights")
        
        # Get recent analytics data
        recent_learning_analytics = LearningAnalytics.objects.all().order_by('-date')[:100]
        recent_performance_metrics = PerformanceMetrics.objects.all().order_by('-period_end')[:50]
        
        # Generate insights (simplified - in real app, this would use AI)
        insights = self.generate_insights(recent_learning_analytics, recent_performance_metrics)
        
        return Response({
            'insights': insights,
            'data_sources': ['learning_analytics', 'performance_metrics'],
            'generated_at': timezone.now()
        })
    
    def generate_insights(self, learning_analytics, performance_metrics):
        """Generate insights from analytics data"""
        insights = []
        
        # Learning time insights
        if learning_analytics:
            avg_learning_time = learning_analytics.aggregate(
                avg=models.Avg('total_learning_time')
            )['avg'] or 0
            
            if avg_learning_time > 120:  # 2 hours
                insights.append({
                    'type': 'positive',
                    'category': 'learning_time',
                    'message': f"Students are spending an average of {avg_learning_time:.1f} minutes learning, which is excellent engagement.",
                    'recommendation': "Consider providing more challenging content to maintain engagement."
                })
            elif avg_learning_time < 60:  # 1 hour
                insights.append({
                    'type': 'warning',
                    'category': 'learning_time',
                    'message': f"Average learning time is {avg_learning_time:.1f} minutes, which may indicate low engagement.",
                    'recommendation': "Review content difficulty and consider adding interactive elements."
                })
        
        # Performance insights
        if performance_metrics:
            avg_grade = performance_metrics.aggregate(
                avg=models.Avg('overall_grade')
            )['avg'] or 0
            
            if avg_grade > 3.5:
                insights.append({
                    'type': 'positive',
                    'category': 'performance',
                    'message': f"Class average grade is {avg_grade:.2f}, indicating strong academic performance.",
                    'recommendation': "Consider introducing advanced topics to challenge high-performing students."
                })
            elif avg_grade < 2.5:
                insights.append({
                    'type': 'warning',
                    'category': 'performance',
                    'message': f"Class average grade is {avg_grade:.2f}, which may indicate learning difficulties.",
                    'recommendation': "Review curriculum and consider additional support resources."
                })
        
        return insights


# Legacy view for backward compatibility
def analytics_list(request):
    return JsonResponse({'message': 'Use API endpoints for analytics data'})
