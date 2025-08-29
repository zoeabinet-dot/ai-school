from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
import json
import openai
from django.conf import settings

from .models import (
    AITeacherProfile, Conversation, Message, LearningRecommendation,
    AIFeedback, AITeachingSession, StudentAIInteraction
)
from accounts.models import Student


class ConversationViewSet(viewsets.ModelViewSet):
    """AI conversation viewset"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Conversation.objects.filter(student__user=user)
        elif user.role in ['staff', 'admin']:
            return Conversation.objects.all()
        return Conversation.objects.none()


class LearningRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """Learning recommendation viewset"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return LearningRecommendation.objects.filter(
                student__user=user,
                is_dismissed=False
            ).order_by('-created_at')
        elif user.role in ['staff', 'admin']:
            return LearningRecommendation.objects.all()
        return LearningRecommendation.objects.none()


class AIFeedbackViewSet(viewsets.ReadOnlyModelViewSet):
    """AI feedback viewset"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return AIFeedback.objects.filter(student__user=user).order_by('-created_at')
        elif user.role in ['staff', 'admin']:
            return AIFeedback.objects.all()
        return AIFeedback.objects.none()


class AIChatView(generics.CreateAPIView):
    """AI chat endpoint"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can chat with AI teacher'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student = request.user.student_profile
        message_content = request.data.get('message', '')
        conversation_id = request.data.get('conversation_id')
        
        if not message_content:
            return Response(
                {'error': 'Message content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create conversation
        if conversation_id:
            try:
                conversation = Conversation.objects.get(
                    id=conversation_id,
                    student=student
                )
            except Conversation.DoesNotExist:
                return Response(
                    {'error': 'Conversation not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Create new conversation
            ai_teacher = AITeacherProfile.objects.filter(is_active=True).first()
            if not ai_teacher:
                return Response(
                    {'error': 'No AI teacher available'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            conversation = Conversation.objects.create(
                student=student,
                ai_teacher=ai_teacher,
                conversation_type='general_question',
                title=message_content[:50] + '...' if len(message_content) > 50 else message_content
            )
        
        # Save student message
        student_message = Message.objects.create(
            conversation=conversation,
            sender='student',
            content=message_content
        )
        
        # Generate AI response
        try:
            ai_response_content = self._generate_ai_response(
                conversation, 
                message_content,
                student
            )
            
            # Save AI message
            ai_message = Message.objects.create(
                conversation=conversation,
                sender='ai',
                content=ai_response_content
            )
            
            # Record interaction
            StudentAIInteraction.objects.create(
                student=student,
                interaction_type='question_asked',
                conversation=conversation
            )
            
            return Response({
                'conversation_id': conversation.id,
                'student_message': {
                    'id': student_message.id,
                    'content': student_message.content,
                    'timestamp': student_message.timestamp
                },
                'ai_response': {
                    'id': ai_message.id,
                    'content': ai_message.content,
                    'timestamp': ai_message.timestamp
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to generate AI response: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _generate_ai_response(self, conversation, message, student):
        """Generate AI response using OpenAI"""
        try:
            # Set up OpenAI client
            openai.api_key = settings.OPENAI_API_KEY
            
            # Build conversation context
            recent_messages = Message.objects.filter(
                conversation=conversation
            ).order_by('timestamp')[-10:]  # Last 10 messages for context
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are an AI teacher helping {student.user.get_full_name()}, 
                    a {student.grade_level} grade student. Be encouraging, patient, and educational. 
                    Adapt your language to their grade level. Focus on helping them learn and understand concepts."""
                }
            ]
            
            # Add conversation history
            for msg in recent_messages[:-1]:  # Exclude the current message
                role = "user" if msg.sender == 'student' else "assistant"
                messages.append({
                    "role": role,
                    "content": msg.content
                })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Generate response
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # Fallback response
            return f"I'm sorry, I'm having trouble right now. Could you please try asking your question again? In the meantime, remember that learning is a journey, and every question you ask helps you grow!"


class VoiceChatView(generics.CreateAPIView):
    """Voice chat with AI teacher"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can use voice chat'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # This would handle voice-to-text conversion and text-to-speech
        # For now, return a placeholder response
        return Response({
            'message': 'Voice chat feature is under development',
            'audio_url': None
        })


class GenerateLessonView(generics.CreateAPIView):
    """Generate AI lesson"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role not in ['staff', 'admin']:
            return Response(
                {'error': 'Only staff can generate lessons'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        topic = request.data.get('topic', '')
        grade_level = request.data.get('grade_level', '')
        duration_minutes = request.data.get('duration_minutes', 30)
        
        if not topic or not grade_level:
            return Response(
                {'error': 'Topic and grade level are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate lesson content using AI
        try:
            lesson_content = self._generate_lesson_content(
                topic, 
                grade_level, 
                duration_minutes
            )
            
            return Response({
                'lesson': lesson_content,
                'generated_at': timezone.now()
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to generate lesson: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _generate_lesson_content(self, topic, grade_level, duration):
        """Generate lesson content using AI"""
        # This would use AI to generate comprehensive lesson content
        # For now, return a structured template
        return {
            'title': f'{topic} - Grade {grade_level}',
            'duration_minutes': duration,
            'objectives': [
                f'Students will understand the basics of {topic}',
                f'Students will be able to apply {topic} concepts',
                f'Students will demonstrate knowledge through examples'
            ],
            'content': {
                'introduction': f'Welcome to our lesson on {topic}!',
                'main_content': f'Let\'s explore {topic} step by step...',
                'activities': [
                    f'Interactive exercise on {topic}',
                    f'Group discussion about {topic} applications',
                    f'Practice problems related to {topic}'
                ],
                'conclusion': f'Today we learned about {topic}. Remember to practice!'
            },
            'resources': [
                f'Additional reading on {topic}',
                f'Practice worksheets for {topic}',
                f'Online videos about {topic}'
            ]
        }


class AnalyzePerformanceView(generics.CreateAPIView):
    """Analyze student performance with AI"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role not in ['staff', 'admin']:
            return Response(
                {'error': 'Access denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student_id = request.data.get('student_id')
        if not student_id:
            return Response(
                {'error': 'Student ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            student = Student.objects.get(id=student_id)
            analysis = self._analyze_student_performance(student)
            
            return Response(analysis)
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def _analyze_student_performance(self, student):
        """Analyze student performance and provide insights"""
        # This would use AI to analyze student performance data
        # For now, return a template analysis
        return {
            'student_name': student.user.get_full_name(),
            'analysis': {
                'strengths': [
                    'Shows consistent effort in assignments',
                    'Good participation in class discussions',
                    'Strong problem-solving skills'
                ],
                'areas_for_improvement': [
                    'Could benefit from more practice in mathematics',
                    'Time management during tests needs improvement',
                    'Reading comprehension could be enhanced'
                ],
                'recommendations': [
                    'Provide additional math practice worksheets',
                    'Implement time management strategies',
                    'Encourage more reading activities'
                ]
            },
            'performance_trend': 'improving',
            'engagement_level': 'high',
            'generated_at': timezone.now()
        }


class AITeachingSessionView(generics.ListCreateAPIView):
    """AI teaching session management"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return AITeachingSession.objects.filter(student__user=user)
        elif user.role in ['staff', 'admin']:
            return AITeachingSession.objects.all()
        return AITeachingSession.objects.none()
    
    def create(self, request, *args, **kwargs):
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can create teaching sessions'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create a new AI teaching session
        student = request.user.student_profile
        session_type = request.data.get('session_type', 'individual_lesson')
        subject_id = request.data.get('subject_id')
        
        try:
            ai_teacher = AITeacherProfile.objects.filter(is_active=True).first()
            if not ai_teacher:
                return Response(
                    {'error': 'No AI teacher available'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            session = AITeachingSession.objects.create(
                student=student,
                ai_teacher=ai_teacher,
                session_type=session_type,
                subject_id=subject_id,
                title=f'{session_type.replace("_", " ").title()} Session',
                scheduled_start=timezone.now(),
                status='in_progress'
            )
            
            return Response({
                'session_id': session.id,
                'status': session.status,
                'message': 'AI teaching session started successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to create session: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )