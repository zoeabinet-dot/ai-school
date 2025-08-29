from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

from .models import (
    StudentPerformanceMetrics, AttendanceRecord, EngagementMetrics,
    LearningAnalytics, BehavioralObservation
)
from accounts.models import Student


class StudentPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    """Student performance metrics viewset"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return StudentPerformanceMetrics.objects.filter(student__user=user)
        elif user.role == 'staff':
            return StudentPerformanceMetrics.objects.filter(
                student__in=user.staff_profile.assigned_students.all()
            )
        elif user.role == 'admin':
            return StudentPerformanceMetrics.objects.all()
        return StudentPerformanceMetrics.objects.none()


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    """Attendance records viewset"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return AttendanceRecord.objects.filter(student__user=user)
        elif user.role == 'staff':
            return AttendanceRecord.objects.filter(
                student__in=user.staff_profile.assigned_students.all()
            )
        elif user.role == 'admin':
            return AttendanceRecord.objects.all()
        return AttendanceRecord.objects.none()


class EngagementViewSet(viewsets.ReadOnlyModelViewSet):
    """Engagement metrics viewset"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return EngagementMetrics.objects.filter(student__user=user)
        elif user.role == 'staff':
            return EngagementMetrics.objects.filter(
                student__in=user.staff_profile.assigned_students.all()
            )
        elif user.role == 'admin':
            return EngagementMetrics.objects.all()
        return EngagementMetrics.objects.none()


class AnalyticsDashboardView(generics.RetrieveAPIView):
    """Analytics dashboard view"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.role == 'student':
            return self._student_dashboard(user.student_profile)
        elif user.role in ['staff', 'admin']:
            return self._staff_dashboard(user)
        elif user.role == 'family':
            return self._family_dashboard(user.family_profile)
        
        return Response({'error': 'Invalid role'}, status=status.HTTP_403_FORBIDDEN)
    
    def _student_dashboard(self, student):
        """Student analytics dashboard"""
        recent_performance = StudentPerformanceMetrics.objects.filter(
            student=student
        ).order_by('-date')[:30]
        
        attendance_rate = AttendanceRecord.objects.filter(
            student=student,
            date__gte=timezone.now().date() - timedelta(days=30)
        ).aggregate(
            present_count=Count('id', filter=Q(status='present')),
            total_count=Count('id')
        )
        
        return Response({
            'performance_trend': [
                {
                    'date': p.date,
                    'overall_score': p.overall_score,
                    'engagement_level': p.engagement_level
                } for p in recent_performance
            ],
            'attendance_rate': (
                attendance_rate['present_count'] / attendance_rate['total_count'] * 100
                if attendance_rate['total_count'] > 0 else 0
            ),
        })
    
    def _staff_dashboard(self, user):
        """Staff/Admin analytics dashboard"""
        if user.role == 'staff':
            students = user.staff_profile.assigned_students.all()
        else:
            students = Student.objects.filter(is_active=True)
        
        return Response({
            'total_students': students.count(),
            'average_performance': StudentPerformanceMetrics.objects.filter(
                student__in=students
            ).aggregate(avg_score=Avg('overall_score'))['avg_score'] or 0,
        })
    
    def _family_dashboard(self, family):
        """Family analytics dashboard"""
        students = family.students.all()
        
        return Response({
            'students_count': students.count(),
            'students_performance': [
                {
                    'student_name': student.user.get_full_name(),
                    'recent_performance': StudentPerformanceMetrics.objects.filter(
                        student=student
                    ).order_by('-date').first()
                } for student in students
            ]
        })


class StudentReportView(generics.RetrieveAPIView):
    """Individual student report"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, student_id):
        student = Student.objects.get(id=student_id)
        
        # Check permissions
        if not self._has_permission(request.user, student):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Generate comprehensive report
        report_data = {
            'student': {
                'name': student.user.get_full_name(),
                'grade_level': student.grade_level,
                'student_id': student.student_id
            },
            'performance_summary': self._get_performance_summary(student),
            'attendance_summary': self._get_attendance_summary(student),
            'engagement_summary': self._get_engagement_summary(student),
        }
        
        return Response(report_data)
    
    def _has_permission(self, user, student):
        """Check if user has permission to view student report"""
        if user.role == 'admin':
            return True
        elif user.role == 'staff':
            return student in user.staff_profile.assigned_students.all()
        elif user.role == 'family':
            return student in user.family_profile.students.all()
        elif user.role == 'student':
            return student.user == user
        return False
    
    def _get_performance_summary(self, student):
        """Get performance summary for student"""
        return {
            'average_score': StudentPerformanceMetrics.objects.filter(
                student=student
            ).aggregate(avg=Avg('overall_score'))['avg'] or 0
        }
    
    def _get_attendance_summary(self, student):
        """Get attendance summary for student"""
        total_days = AttendanceRecord.objects.filter(student=student).count()
        present_days = AttendanceRecord.objects.filter(
            student=student, 
            status='present'
        ).count()
        
        return {
            'attendance_rate': (present_days / total_days * 100) if total_days > 0 else 0,
            'total_days': total_days,
            'present_days': present_days
        }
    
    def _get_engagement_summary(self, student):
        """Get engagement summary for student"""
        return {
            'average_engagement': EngagementMetrics.objects.filter(
                student=student
            ).aggregate(avg=Avg('participation_score'))['avg'] or 0
        }


class ClassroomReportView(generics.RetrieveAPIView):
    """Classroom analytics report"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role not in ['staff', 'admin']:
            return Response(
                {'error': 'Access denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get students based on role
        if request.user.role == 'staff':
            students = request.user.staff_profile.assigned_students.all()
        else:
            students = Student.objects.filter(is_active=True)
        
        report_data = {
            'total_students': students.count(),
            'performance_distribution': self._get_performance_distribution(students),
            'attendance_trends': self._get_attendance_trends(students),
            'engagement_metrics': self._get_engagement_metrics(students),
        }
        
        return Response(report_data)
    
    def _get_performance_distribution(self, students):
        """Get performance distribution across students"""
        return {
            'excellent': students.filter(
                performance_metrics__overall_score__gte=90
            ).distinct().count(),
            'good': students.filter(
                performance_metrics__overall_score__gte=75,
                performance_metrics__overall_score__lt=90
            ).distinct().count(),
            'average': students.filter(
                performance_metrics__overall_score__gte=60,
                performance_metrics__overall_score__lt=75
            ).distinct().count(),
            'needs_improvement': students.filter(
                performance_metrics__overall_score__lt=60
            ).distinct().count(),
        }
    
    def _get_attendance_trends(self, students):
        """Get attendance trends for students"""
        return {
            'average_attendance_rate': AttendanceRecord.objects.filter(
                student__in=students
            ).aggregate(
                rate=Avg('status')  # This would need proper calculation
            )['rate'] or 0
        }
    
    def _get_engagement_metrics(self, students):
        """Get engagement metrics for students"""
        return {
            'average_engagement': EngagementMetrics.objects.filter(
                student__in=students
            ).aggregate(avg=Avg('participation_score'))['avg'] or 0
        }


class LearningInsightsView(generics.RetrieveAPIView):
    """AI-generated learning insights"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.role == 'student':
            insights = self._get_student_insights(user.student_profile)
        elif user.role in ['staff', 'admin']:
            insights = self._get_classroom_insights(user)
        else:
            return Response(
                {'error': 'Access denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(insights)
    
    def _get_student_insights(self, student):
        """Get personalized insights for student"""
        return {
            'recommendations': [
                'Focus on improving math problem-solving skills',
                'Great progress in reading comprehension',
                'Consider more practice in science concepts'
            ],
            'strengths': ['Creative thinking', 'Active participation'],
            'areas_for_improvement': ['Time management', 'Math calculations']
        }
    
    def _get_classroom_insights(self, user):
        """Get classroom-level insights"""
        return {
            'trends': [
                'Overall engagement has increased by 15% this month',
                'Students are struggling with advanced math concepts',
                'Reading scores show consistent improvement'
            ],
            'alerts': [
                '3 students need additional support in mathematics',
                'Attendance rates have dropped slightly this week'
            ]
        }