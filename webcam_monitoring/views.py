from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
import uuid
import cv2
import numpy as np

from .models import (
    WebcamSession, AttentionAnalysis, EmotionAnalysis, BehaviorAnalysis,
    AlertEvent, MonitoringSettings, MonitoringReport
)
from accounts.models import Student


class WebcamSessionViewSet(viewsets.ModelViewSet):
    """Webcam session viewset"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return WebcamSession.objects.filter(student__user=user)
        elif user.role in ['staff', 'admin']:
            return WebcamSession.objects.all()
        return WebcamSession.objects.none()


class AlertEventViewSet(viewsets.ReadOnlyModelViewSet):
    """Alert event viewset"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return AlertEvent.objects.filter(webcam_session__student__user=user)
        elif user.role in ['staff', 'admin']:
            return AlertEvent.objects.all()
        return AlertEvent.objects.none()


class MonitoringReportViewSet(viewsets.ReadOnlyModelViewSet):
    """Monitoring report viewset"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return MonitoringReport.objects.filter(student__user=user)
        elif user.role in ['staff', 'admin']:
            return MonitoringReport.objects.all()
        return MonitoringReport.objects.none()


class StartMonitoringView(generics.CreateAPIView):
    """Start webcam monitoring session"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can start monitoring sessions'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student = request.user.student_profile
        
        # Check if student has given consent
        try:
            settings = MonitoringSettings.objects.get(student=student)
            if not settings.monitoring_enabled or not settings.student_consent:
                return Response(
                    {'error': 'Monitoring not enabled or consent not given'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except MonitoringSettings.DoesNotExist:
            return Response(
                {'error': 'Monitoring settings not configured'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for active session
        active_session = WebcamSession.objects.filter(
            student=student,
            status='active'
        ).first()
        
        if active_session:
            return Response(
                {
                    'error': 'An active monitoring session already exists',
                    'session_id': active_session.session_id
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new session
        session = WebcamSession.objects.create(
            student=student,
            session_id=str(uuid.uuid4()),
            lesson_id=request.data.get('lesson_id'),
            subject_id=request.data.get('subject_id'),
            consent_given=True,
            consent_timestamp=timezone.now(),
            face_detection_enabled=settings.face_detection,
            emotion_analysis_enabled=settings.emotion_analysis,
            attention_tracking_enabled=settings.attention_tracking,
            posture_analysis_enabled=settings.posture_monitoring
        )
        
        return Response({
            'session_id': session.session_id,
            'status': session.status,
            'message': 'Monitoring session started successfully'
        }, status=status.HTTP_201_CREATED)


class EndMonitoringView(generics.CreateAPIView):
    """End webcam monitoring session"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can end monitoring sessions'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        session_id = request.data.get('session_id')
        if not session_id:
            return Response(
                {'error': 'Session ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            session = WebcamSession.objects.get(
                session_id=session_id,
                student__user=request.user,
                status='active'
            )
            
            # End session
            session.status = 'completed'
            session.ended_at = timezone.now()
            
            # Calculate duration
            if session.started_at:
                duration = session.ended_at - session.started_at
                session.duration_minutes = int(duration.total_seconds() / 60)
            
            session.save()
            
            return Response({
                'message': 'Monitoring session ended successfully',
                'duration_minutes': session.duration_minutes
            })
            
        except WebcamSession.DoesNotExist:
            return Response(
                {'error': 'Active session not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class AnalyzeFrameView(generics.CreateAPIView):
    """Analyze webcam frame for attention and emotion"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can submit frames for analysis'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        session_id = request.data.get('session_id')
        frame_data = request.data.get('frame_data')  # Base64 encoded image
        
        if not session_id or not frame_data:
            return Response(
                {'error': 'Session ID and frame data are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            session = WebcamSession.objects.get(
                session_id=session_id,
                student__user=request.user,
                status='active'
            )
            
            # Analyze frame (simplified implementation)
            analysis_results = self._analyze_frame(frame_data, session)
            
            return Response(analysis_results)
            
        except WebcamSession.DoesNotExist:
            return Response(
                {'error': 'Active session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def _analyze_frame(self, frame_data, session):
        """Analyze webcam frame for attention and emotion"""
        try:
            # This is a simplified implementation
            # In production, this would use computer vision models
            
            # Mock analysis results
            attention_score = np.random.uniform(60, 95)  # Random score for demo
            emotion = np.random.choice(['happy', 'neutral', 'confused', 'focused'])
            engagement_level = 'high' if attention_score > 80 else 'medium' if attention_score > 60 else 'low'
            
            # Save attention analysis
            if session.attention_tracking_enabled:
                AttentionAnalysis.objects.create(
                    webcam_session=session,
                    attention_level=engagement_level,
                    attention_score=attention_score,
                    focus_duration_seconds=30,  # Mock duration
                    gaze_direction='center',
                    confidence_score=0.85
                )
            
            # Save emotion analysis
            if session.emotion_analysis_enabled:
                EmotionAnalysis.objects.create(
                    webcam_session=session,
                    dominant_emotion=emotion,
                    emotion_scores={emotion: 0.8, 'neutral': 0.2},
                    emotion_confidence=0.85,
                    engagement_level=engagement_level,
                    engagement_score=attention_score
                )
            
            # Check for alerts
            alerts = []
            if attention_score < 50:
                alert = AlertEvent.objects.create(
                    webcam_session=session,
                    alert_type='attention_drop',
                    severity='medium',
                    message='Student attention level has dropped significantly',
                    trigger_data={'attention_score': attention_score}
                )
                alerts.append({
                    'type': alert.alert_type,
                    'message': alert.message,
                    'severity': alert.severity
                })
            
            return {
                'analysis': {
                    'attention_score': attention_score,
                    'emotion': emotion,
                    'engagement_level': engagement_level,
                    'gaze_direction': 'center'
                },
                'alerts': alerts,
                'timestamp': timezone.now()
            }
            
        except Exception as e:
            return {
                'error': f'Analysis failed: {str(e)}',
                'timestamp': timezone.now()
            }


class MonitoringSettingsView(generics.RetrieveUpdateAPIView):
    """Monitoring settings view"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if self.request.user.role == 'student':
            student = self.request.user.student_profile
            settings, created = MonitoringSettings.objects.get_or_create(
                student=student
            )
            return settings
        return None
    
    def get(self, request):
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can view monitoring settings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        settings = self.get_object()
        return Response({
            'monitoring_enabled': settings.monitoring_enabled,
            'student_consent': settings.student_consent,
            'parent_consent': settings.parent_consent,
            'face_detection': settings.face_detection,
            'emotion_analysis': settings.emotion_analysis,
            'attention_tracking': settings.attention_tracking,
            'behavior_analysis': settings.behavior_analysis,
            'real_time_alerts': settings.real_time_alerts,
            'data_retention_days': settings.data_retention_days
        })
    
    def patch(self, request):
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can update monitoring settings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        settings = self.get_object()
        
        # Update allowed settings
        allowed_fields = [
            'face_detection', 'emotion_analysis', 'attention_tracking',
            'behavior_analysis', 'real_time_alerts'
        ]
        
        for field in allowed_fields:
            if field in request.data:
                setattr(settings, field, request.data[field])
        
        settings.updated_at = timezone.now()
        settings.save()
        
        return Response({
            'message': 'Settings updated successfully'
        })


class ConsentView(generics.CreateAPIView):
    """Consent management view"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role not in ['student', 'family']:
            return Response(
                {'error': 'Only students and families can provide consent'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        consent_type = request.data.get('consent_type')  # 'student' or 'parent'
        consent_given = request.data.get('consent_given', False)
        student_id = request.data.get('student_id')
        
        if request.user.role == 'student':
            student = request.user.student_profile
        elif request.user.role == 'family':
            if not student_id:
                return Response(
                    {'error': 'Student ID is required for family consent'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                student = request.user.family_profile.students.get(id=student_id)
            except:
                return Response(
                    {'error': 'Student not found in family'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Get or create settings
        settings, created = MonitoringSettings.objects.get_or_create(
            student=student
        )
        
        # Update consent
        if consent_type == 'student' and request.user.role == 'student':
            settings.student_consent = consent_given
        elif consent_type == 'parent' and request.user.role == 'family':
            settings.parent_consent = consent_given
        else:
            return Response(
                {'error': 'Invalid consent type for user role'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Enable monitoring if both consents are given
        settings.monitoring_enabled = settings.student_consent and settings.parent_consent
        settings.save()
        
        return Response({
            'message': 'Consent updated successfully',
            'monitoring_enabled': settings.monitoring_enabled,
            'student_consent': settings.student_consent,
            'parent_consent': settings.parent_consent
        })