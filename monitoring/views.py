from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import models
import json
# import cv2  # Uncomment when OpenCV is needed for production
# import numpy as np  # Uncomment when numpy is needed for production
from datetime import datetime, timedelta

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import (
    WebcamSession, FrameAnalysis, BehaviorEvent, PrivacySettings, MonitoringAlert
)
from .serializers import (
    WebcamSessionSerializer, FrameAnalysisSerializer, BehaviorEventSerializer,
    PrivacySettingsSerializer, MonitoringAlertSerializer
)
from students.models import Student
from accounts.models import User


class WebcamSessionListView(APIView):
    """
    List webcam monitoring sessions with filtering options
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or request.user.is_family):
            raise PermissionDenied("Insufficient permissions to view monitoring sessions")
        
        sessions = WebcamSession.objects.all()
        
        # Apply filters
        student_id = request.query_params.get('student_id')
        session_type = request.query_params.get('session_type')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        status_filter = request.query_params.get('status')
        
        if student_id:
            sessions = sessions.filter(student_id=student_id)
        if session_type:
            sessions = sessions.filter(session_type=session_type)
        if date_from:
            sessions = sessions.filter(start_time__gte=date_from)
        if date_to:
            sessions = sessions.filter(end_time__lte=date_to)
        if status_filter:
            sessions = sessions.filter(status=status_filter)
        
        # Role-based filtering
        if request.user.is_family:
            # Family can only see their own students' sessions
            student_ids = request.user.family_students.values_list('id', flat=True)
            sessions = sessions.filter(student_id__in=student_ids)
        elif request.user.is_staff_member:
            # Staff can see sessions for students in their assigned classes
            assigned_grades = request.user.staff_profile.assigned_grades
            sessions = sessions.filter(student__grade_level__in=assigned_grades)
        
        serializer = WebcamSessionSerializer(sessions, many=True)
        return Response(serializer.data)


class WebcamSessionCreateView(APIView):
    """
    Create a new webcam monitoring session
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create monitoring sessions")
        
        data = request.data.copy()
        data['start_time'] = timezone.now()
        data['status'] = 'active'
        
        serializer = WebcamSessionSerializer(data=data)
        if serializer.is_valid():
            session = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WebcamSessionDetailView(APIView):
    """
    Get detailed information about a webcam session
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        session = get_object_or_404(WebcamSession, pk=pk)
        
        # Check permissions
        if not self.can_view_session(request.user, session):
            raise PermissionDenied("Insufficient permissions to view this session")
        
        serializer = WebcamSessionSerializer(session)
        return Response(serializer.data)
    
    def can_view_session(self, user, session):
        if user.is_admin or user.is_staff_member:
            return True
        elif user.is_family:
            return session.student.family == user
        elif user.is_student:
            return session.student.user == user
        return False


class WebcamSessionEndView(APIView):
    """
    End a webcam monitoring session
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        session = get_object_or_404(WebcamSession, pk=pk)
        
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can end monitoring sessions")
        
        session.end_time = timezone.now()
        session.duration = (session.end_time - session.start_time).total_seconds() / 60  # in minutes
        session.status = 'completed'
        session.save()
        
        serializer = WebcamSessionSerializer(session)
        return Response(serializer.data)


class FrameAnalysisListView(APIView):
    """
    List frame analysis results for a session
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, session_id):
        session = get_object_or_404(WebcamSession, pk=session_id)
        
        # Check permissions
        if not self.can_view_session(request.user, session):
            raise PermissionDenied("Insufficient permissions to view this session's analysis")
        
        analyses = FrameAnalysis.objects.filter(session=session)
        
        # Apply filters
        analysis_type = request.query_params.get('analysis_type')
        confidence_min = request.query_params.get('confidence_min')
        timestamp_from = request.query_params.get('timestamp_from')
        timestamp_to = request.query_params.get('timestamp_to')
        
        if analysis_type:
            analyses = analyses.filter(analysis_type=analysis_type)
        if confidence_min:
            analyses = analyses.filter(confidence_score__gte=float(confidence_min))
        if timestamp_from:
            analyses = analyses.filter(timestamp__gte=timestamp_from)
        if timestamp_to:
            analyses = analyses.filter(timestamp__lte=timestamp_to)
        
        serializer = FrameAnalysisSerializer(analyses, many=True)
        return Response(serializer.data)


class FrameAnalysisCreateView(APIView):
    """
    Create new frame analysis results
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, session_id):
        session = get_object_or_404(WebcamSession, pk=session_id)
        
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create frame analysis")
        
        data = request.data.copy()
        data['session'] = session.id
        data['timestamp'] = timezone.now()
        
        serializer = FrameAnalysisSerializer(data=data)
        if serializer.is_valid():
            analysis = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BehaviorEventListView(APIView):
    """
    List behavior events detected during monitoring
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or request.user.is_family):
            raise PermissionDenied("Insufficient permissions to view behavior events")
        
        events = BehaviorEvent.objects.all()
        
        # Apply filters
        student_id = request.query_params.get('student_id')
        event_type = request.query_params.get('event_type')
        severity = request.query_params.get('severity')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        if student_id:
            events = events.filter(student_id=student_id)
        if event_type:
            events = events.filter(event_type=event_type)
        if severity:
            events = events.filter(severity=severity)
        if date_from:
            events = events.filter(timestamp__gte=date_from)
        if date_to:
            events = events.filter(timestamp__lte=date_to)
        
        # Role-based filtering
        if request.user.is_family:
            student_ids = request.user.family_students.values_list('id', flat=True)
            events = events.filter(student_id__in=student_ids)
        elif request.user.is_staff_member:
            assigned_grades = request.user.staff_profile.assigned_grades
            events = events.filter(student__grade_level__in=assigned_grades)
        
        serializer = BehaviorEventSerializer(events, many=True)
        return Response(serializer.data)


class BehaviorEventCreateView(APIView):
    """
    Create new behavior event
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create behavior events")
        
        data = request.data.copy()
        data['timestamp'] = timezone.now()
        
        serializer = BehaviorEventSerializer(data=data)
        if serializer.is_valid():
            event = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrivacySettingsListView(APIView):
    """
    List privacy settings for users
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Users can only see their own privacy settings
        settings = PrivacySettings.objects.filter(user=request.user)
        serializer = PrivacySettingsSerializer(settings, many=True)
        return Response(serializer.data)


class PrivacySettingsCreateView(APIView):
    """
    Create new privacy settings
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        
        serializer = PrivacySettingsSerializer(data=data)
        if serializer.is_valid():
            settings = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrivacySettingsUpdateView(APIView):
    """
    Update privacy settings
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        settings = get_object_or_404(PrivacySettings, pk=pk, user=request.user)
        
        serializer = PrivacySettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            settings = serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MonitoringAlertListView(APIView):
    """
    List monitoring alerts
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin or request.user.is_family):
            raise PermissionDenied("Insufficient permissions to view monitoring alerts")
        
        alerts = MonitoringAlert.objects.all()
        
        # Apply filters
        alert_type = request.query_params.get('alert_type')
        severity = request.query_params.get('severity')
        status_filter = request.query_params.get('status')
        student_id = request.query_params.get('student_id')
        
        if alert_type:
            alerts = alerts.filter(alert_type=alert_type)
        if severity:
            alerts = alerts.filter(severity=severity)
        if status_filter:
            alerts = alerts.filter(status=status_filter)
        if student_id:
            alerts = alerts.filter(student_id=student_id)
        
        # Role-based filtering
        if request.user.is_family:
            student_ids = request.user.family_students.values_list('id', flat=True)
            alerts = alerts.filter(student_id__in=student_ids)
        elif request.user.is_staff_member:
            assigned_grades = request.user.staff_profile.assigned_grades
            alerts = alerts.filter(student__grade_level__in=assigned_grades)
        
        serializer = MonitoringAlertSerializer(alerts, many=True)
        return Response(serializer.data)


class MonitoringAlertCreateView(APIView):
    """
    Create new monitoring alert
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create monitoring alerts")
        
        data = request.data.copy()
        data['timestamp'] = timezone.now()
        data['status'] = 'active'
        
        serializer = MonitoringAlertSerializer(data=data)
        if serializer.is_valid():
            alert = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MonitoringAlertUpdateView(APIView):
    """
    Update monitoring alert status
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        alert = get_object_or_404(MonitoringAlert, pk=pk)
        
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can update monitoring alerts")
        
        serializer = MonitoringAlertSerializer(alert, data=request.data, partial=True)
        if serializer.is_valid():
            alert = serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentMonitoringDashboardView(APIView):
    """
    Get comprehensive monitoring dashboard for a specific student
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Check permissions
        if not self.can_view_student_monitoring(request.user, student):
            raise PermissionDenied("Insufficient permissions to view this student's monitoring")
        
        # Get recent monitoring sessions
        recent_sessions = WebcamSession.objects.filter(student=student).order_by('-start_time')[:10]
        
        # Get recent behavior events
        recent_events = BehaviorEvent.objects.filter(student=student).order_by('-timestamp')[:20]
        
        # Get active alerts
        active_alerts = MonitoringAlert.objects.filter(student=student, status='active')
        
        # Get privacy settings
        privacy_settings = PrivacySettings.objects.filter(user=student.user).first()
        
        # Calculate monitoring statistics
        total_sessions = WebcamSession.objects.filter(student=student).count()
        total_duration = sum([s.duration or 0 for s in WebcamSession.objects.filter(student=student)])
        total_events = BehaviorEvent.objects.filter(student=student).count()
        active_alerts_count = active_alerts.count()
        
        dashboard_data = {
            'student': {
                'id': student.id,
                'name': student.user.get_full_name(),
                'grade_level': student.grade_level
            },
            'recent_sessions': WebcamSessionSerializer(recent_sessions, many=True).data,
            'recent_events': BehaviorEventSerializer(recent_events, many=True).data,
            'active_alerts': MonitoringAlertSerializer(active_alerts, many=True).data,
            'privacy_settings': PrivacySettingsSerializer(privacy_settings).data if privacy_settings else None,
            'monitoring_statistics': {
                'total_sessions': total_sessions,
                'total_duration_minutes': total_duration,
                'total_behavior_events': total_events,
                'active_alerts': active_alerts_count,
                'last_session': recent_sessions.first().end_time if recent_sessions.exists() else None
            }
        }
        
        return Response(dashboard_data)
    
    def can_view_student_monitoring(self, user, student):
        if user.is_admin or user.is_staff_member:
            return True
        elif user.is_family:
            return student.family == user
        elif user.is_student:
            return student.user == user
        return False


class RealTimeMonitoringView(APIView):
    """
    Real-time monitoring stream (placeholder for WebSocket implementation)
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, session_id):
        session = get_object_or_404(WebcamSession, pk=session_id)
        
        # Check permissions
        if not self.can_view_session(request.user, session):
            raise PermissionDenied("Insufficient permissions to view this session")
        
        # This is a placeholder for real-time monitoring
        # In a real implementation, this would use WebSockets or Server-Sent Events
        return Response({
            'message': 'Real-time monitoring endpoint',
            'session_id': session_id,
            'status': 'active',
            'note': 'This endpoint is a placeholder for WebSocket-based real-time monitoring'
        })


class BehaviorAnalysisView(APIView):
    """
    AI-powered behavior analysis from monitoring data
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can perform behavior analysis")
        
        student_id = request.data.get('student_id')
        session_id = request.data.get('session_id')
        analysis_type = request.data.get('analysis_type', 'comprehensive')
        
        if not student_id:
            return Response({'error': 'Student ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        student = get_object_or_404(Student, pk=student_id)
        
        # Get monitoring data for analysis
        sessions = WebcamSession.objects.filter(student=student)
        if session_id:
            sessions = sessions.filter(id=session_id)
        
        events = BehaviorEvent.objects.filter(student=student)
        if session_id:
            events = events.filter(session_id=session_id)
        
        # Perform behavior analysis (simplified - in real app, this would use AI)
        analysis_result = self.analyze_behavior(sessions, events, analysis_type)
        
        return Response({
            'student_id': student_id,
            'session_id': session_id,
            'analysis_type': analysis_type,
            'analysis_result': analysis_result,
            'timestamp': timezone.now()
        })
    
    def analyze_behavior(self, sessions, events, analysis_type):
        """Analyze behavior patterns from monitoring data"""
        analysis = {
            'total_sessions': sessions.count(),
            'total_events': events.count(),
            'session_duration_avg': 0,
            'event_frequency': 0,
            'behavior_patterns': [],
            'recommendations': []
        }
        
        if sessions.exists():
            total_duration = sum([s.duration or 0 for s in sessions])
            analysis['session_duration_avg'] = round(total_duration / sessions.count(), 2)
        
        if events.exists():
            # Calculate event frequency per session
            if analysis['total_sessions'] > 0:
                analysis['event_frequency'] = round(analysis['total_events'] / analysis['total_sessions'], 2)
            
            # Analyze event patterns
            event_types = events.values('event_type').annotate(count=models.Count('id'))
            analysis['behavior_patterns'] = [
                {
                    'event_type': item['event_type'],
                    'count': item['count'],
                    'percentage': round((item['count'] / analysis['total_events']) * 100, 2)
                }
                for item in event_types
            ]
        
        # Generate recommendations based on analysis
        if analysis['event_frequency'] > 5:
            analysis['recommendations'].append({
                'type': 'warning',
                'message': 'High frequency of behavior events detected',
                'action': 'Consider reviewing learning environment and content difficulty'
            })
        
        if analysis['session_duration_avg'] < 30:
            analysis['recommendations'].append({
                'type': 'info',
                'message': 'Short average session duration',
                'action': 'Review content engagement and consider shorter learning segments'
            })
        
        return analysis


class PrivacyComplianceView(APIView):
    """
    Check privacy compliance for monitoring activities
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can check privacy compliance")
        
        # Get all active monitoring sessions
        active_sessions = WebcamSession.objects.filter(status='active')
        
        compliance_report = self.check_compliance(active_sessions)
        
        return Response({
            'compliance_report': compliance_report,
            'timestamp': timezone.now()
        })
    
    def check_compliance(self, active_sessions):
        """Check privacy compliance for monitoring sessions"""
        compliance = {
            'total_sessions': active_sessions.count(),
            'compliant_sessions': 0,
            'non_compliant_sessions': 0,
            'compliance_issues': [],
            'overall_compliance': 0
        }
        
        for session in active_sessions:
            # Check if student has given consent
            privacy_settings = PrivacySettings.objects.filter(user=session.student.user).first()
            
            if privacy_settings and privacy_settings.webcam_monitoring_consent:
                compliance['compliant_sessions'] += 1
            else:
                compliance['non_compliant_sessions'] += 1
                compliance['compliance_issues'].append({
                    'session_id': session.id,
                    'student_id': session.student.id,
                    'issue': 'Missing webcam monitoring consent',
                    'severity': 'high'
                })
        
        if compliance['total_sessions'] > 0:
            compliance['overall_compliance'] = round(
                (compliance['compliant_sessions'] / compliance['total_sessions']) * 100, 2
            )
        
        return compliance


# Legacy view for backward compatibility
def monitoring_list(request):
    return JsonResponse({'message': 'Use API endpoints for monitoring data'})
