from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
import openai
import whisper
import gtts
import os
import tempfile
from datetime import datetime, timedelta

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import (
    AILesson, AIConversation, ConversationMessage, 
    AIRecommendation, AIBehavioralAnalysis,
    LanguagePreference, PredictiveAnalysis, ConversationContext,
    AdvancedBehavioralMetrics, LearningOutcomePrediction
)
from .serializers import (
    AILessonSerializer, AIConversationSerializer, ConversationMessageSerializer,
    AIRecommendationSerializer, AIBehavioralAnalysisSerializer
)
from students.models import Student, LearningSession
from accounts.models import User


class AILessonListView(APIView):
    """
    List all AI lessons with filtering options
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        lessons = AILesson.objects.filter(is_active=True)
        
        # Apply filters
        subject = request.query_params.get('subject')
        grade_level = request.query_params.get('grade_level')
        difficulty = request.query_params.get('difficulty')
        lesson_type = request.query_params.get('lesson_type')
        
        if subject:
            lessons = lessons.filter(subject__icontains=subject)
        if grade_level:
            lessons = lessons.filter(grade_level=grade_level)
        if difficulty:
            lessons = lessons.filter(difficulty_level=difficulty)
        if lesson_type:
            lessons = lessons.filter(lesson_type=lesson_type)
        
        # Role-based filtering
        if request.user.is_student:
            lessons = lessons.filter(grade_level=request.user.student_profile.grade_level)
        elif request.user.is_family:
            # Get lessons for family's students
            student_ids = request.user.family_students.values_list('id', flat=True)
            lessons = lessons.filter(grade_level__in=Student.objects.filter(id__in=student_ids).values_list('grade_level', flat=True))
        
        serializer = AILessonSerializer(lessons, many=True)
        return Response(serializer.data)


class AILessonCreateView(APIView):
    """
    Create a new AI lesson
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can create lessons")
        
        serializer = AILessonSerializer(data=request.data)
        if serializer.is_valid():
            lesson = serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AILessonDetailView(APIView):
    """
    Get detailed information about an AI lesson
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        lesson = get_object_or_404(AILesson, pk=pk, is_active=True)
        
        # Check access permissions
        if request.user.is_student and lesson.grade_level != request.user.student_profile.grade_level:
            raise PermissionDenied("Access denied to this lesson")
        
        serializer = AILessonSerializer(lesson)
        return Response(serializer.data)


class AIConversationListView(APIView):
    """
    List AI conversations for the current user
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_student:
            conversations = AIConversation.objects.filter(student=request.user)
        elif request.user.is_family:
            # Get conversations for family's students
            student_ids = request.user.family_students.values_list('id', flat=True)
            conversations = AIConversation.objects.filter(student_id__in=student_ids)
        elif request.user.is_staff_member:
            # Staff can see conversations for students they're assigned to
            conversations = AIConversation.objects.filter(
                student__in=request.user.assigned_students.all()
            )
        else:
            # Admin can see all conversations
            conversations = AIConversation.objects.all()
        
        serializer = AIConversationSerializer(conversations, many=True)
        return Response(serializer.data)


class AIConversationCreateView(APIView):
    """
    Create a new AI conversation
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Only students can create conversations
        if not request.user.is_student:
            raise PermissionDenied("Only students can create AI conversations")
        
        data = request.data.copy()
        data['student'] = request.user.id
        data['conversation_id'] = str(uuid.uuid4())
        
        serializer = AIConversationSerializer(data=data)
        if serializer.is_valid():
            conversation = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AIConversationDetailView(APIView):
    """
    Get detailed information about an AI conversation
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        conversation = get_object_or_404(AIConversation, pk=pk)
        
        # Check access permissions
        if not self.can_access_conversation(request.user, conversation):
            raise PermissionDenied("Access denied to this conversation")
        
        serializer = AIConversationSerializer(conversation)
        return Response(serializer.data)
    
    def can_access_conversation(self, user, conversation):
        """Check if user can access the conversation"""
        if user.is_admin:
            return True
        if user.is_staff_member and conversation.student in user.assigned_students.all():
            return True
        if user.is_family and conversation.student in user.family_students.all():
            return True
        if user.is_student and conversation.student == user:
            return True
        return False


class ConversationMessageListView(APIView):
    """
    List messages for a conversation
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        conversation = get_object_or_404(AIConversation, pk=pk)
        
        # Check access permissions
        if not self.can_access_conversation(request.user, conversation):
            raise PermissionDenied("Access denied to this conversation")
        
        messages = conversation.messages.all().order_by('sequence_number')
        serializer = ConversationMessageSerializer(messages, many=True)
        return Response(serializer.data)


class SendMessageView(APIView):
    """
    Send a message in an AI conversation
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        conversation = get_object_or_404(AIConversation, pk=pk)
        
        # Check access permissions
        if not self.can_access_conversation(request.user, conversation):
            raise PermissionDenied("Access denied to this conversation")
        
        # Only students can send messages
        if not request.user.is_student:
            raise PermissionDenied("Only students can send messages")
        
        user_message = request.data.get('message', '')
        if not user_message:
            return Response({'error': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Create user message
            user_msg = ConversationMessage.objects.create(
                conversation=conversation,
                content=user_message,
                message_type='user',
                sequence_number=conversation.messages.count() + 1
            )
            
            # Generate AI response
            ai_response = self.generate_ai_response(conversation, user_message)
            
            # Create AI message
            ai_msg = ConversationMessage.objects.create(
                conversation=conversation,
                content=ai_response['content'],
                message_type='ai',
                sequence_number=conversation.messages.count() + 1,
                ai_model_response=ai_response.get('model_response', {}),
                ai_confidence=ai_response.get('confidence', 0),
                processing_time_ms=ai_response.get('processing_time', 0),
                tokens_used=ai_response.get('tokens_used', 0)
            )
            
            return Response({
                'user_message': ConversationMessageSerializer(user_msg).data,
                'ai_response': ConversationMessageSerializer(ai_msg).data
            })
            
        except Exception as e:
            return Response({'error': f'Failed to send message: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def can_access_conversation(self, user, conversation):
        """Check if user can access the conversation"""
        if user.is_admin:
            return True
        if user.is_staff_member and conversation.student in user.assigned_students.all():
            return True
        if user.is_family and conversation.student in user.family_students.all():
            return True
        if user.is_student and conversation.student == user:
            return True
        return False
    
    def generate_ai_response(self, conversation, user_message):
        """Generate AI response using OpenAI or other LLM"""
        try:
            # Configure OpenAI
            if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
                openai.api_key = settings.OPENAI_API_KEY
                
                # Build conversation context
                messages = [
                    {"role": "system", "content": "You are a helpful AI teacher assistant. Provide educational, supportive, and age-appropriate responses."}
                ]
                
                # Add conversation history
                for msg in conversation.messages.all()[:10]:  # Last 10 messages for context
                    role = "user" if msg.message_type == "user" else "assistant"
                    messages.append({"role": role, "content": msg.content})
                
                # Add current user message
                messages.append({"role": "user", "content": user_message})
                
                # Generate response
                start_time = timezone.now()
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7
                )
                end_time = timezone.now()
                
                processing_time = (end_time - start_time).total_seconds() * 1000
                
                return {
                    'content': response.choices[0].message.content,
                    'confidence': 0.9,
                    'processing_time': int(processing_time),
                    'tokens_used': response.usage.total_tokens,
                    'model_response': {
                        'model': response.model,
                        'finish_reason': response.choices[0].finish_reason
                    }
                }
            else:
                # Fallback response
                return {
                    'content': "I'm here to help you learn! What would you like to know?",
                    'confidence': 0.8,
                    'processing_time': 100,
                    'tokens_used': 0
                }
                
        except Exception as e:
            # Fallback response on error
            return {
                'content': "I'm having trouble processing your request right now. Please try again later.",
                'confidence': 0.5,
                'processing_time': 0,
                'tokens_used': 0
            }


class AIRecommendationListView(APIView):
    """
    List AI recommendations for the current user
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_student:
            recommendations = AIRecommendation.objects.filter(student=request.user)
        elif request.user.is_family:
            # Get recommendations for family's students
            student_ids = request.user.family_students.values_list('id', flat=True)
            recommendations = AIRecommendation.objects.filter(student_id__in=student_ids)
        elif request.user.is_staff_member:
            # Staff can see recommendations for students they're assigned to
            recommendations = AIRecommendation.objects.filter(
                student__in=request.user.assigned_students.all()
            )
        else:
            # Admin can see all recommendations
            recommendations = AIRecommendation.objects.all()
        
        # Apply filters
        status_filter = request.query_params.get('status')
        priority_filter = request.query_params.get('priority')
        
        if status_filter:
            recommendations = recommendations.filter(status=status_filter)
        if priority_filter:
            recommendations = recommendations.filter(priority=priority_filter)
        
        serializer = AIRecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)


class GenerateRecommendationView(APIView):
    """
    Generate AI recommendation for a student
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can generate recommendations")
        
        student_id = request.data.get('student_id')
        recommendation_type = request.data.get('type', 'general')
        
        if not student_id:
            return Response({'error': 'Student ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = User.objects.get(id=student_id, role=User.UserRole.STUDENT)
            
            # Generate recommendation using AI
            recommendation_data = self.generate_recommendation(student, recommendation_type)
            
            # Create recommendation record
            recommendation = AIRecommendation.objects.create(
                student=student,
                title=recommendation_data['title'],
                description=recommendation_data['description'],
                recommendation_type=recommendation_type,
                priority=recommendation_data['priority'],
                urgency=recommendation_data['urgency'],
                ai_confidence=recommendation_data['confidence'],
                reasoning=recommendation_data['reasoning'],
                action_items=recommendation_data['action_items']
            )
            
            serializer = AIRecommendationSerializer(recommendation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Failed to generate recommendation: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def generate_recommendation(self, student, recommendation_type):
        """Generate AI recommendation content"""
        try:
            if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
                openai.api_key = settings.OPENAI_API_KEY
                
                prompt = f"""
                Generate a personalized learning recommendation for a student.
                
                Student: {student.get_full_name()}
                Grade: {getattr(student.student_profile, 'grade_level', 'Unknown')}
                Type: {recommendation_type}
                
                Please provide:
                1. A clear title
                2. Detailed description
                3. Priority level (low/medium/high/urgent)
                4. Urgency level (not_urgent/soon/urgent/critical)
                5. Reasoning for the recommendation
                6. Action items as a list
                
                Format as JSON.
                """
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800,
                    temperature=0.7
                )
                
                # Parse AI response
                ai_content = response.choices[0].message.content
                try:
                    # Try to parse as JSON
                    import json
                    parsed = json.loads(ai_content)
                    return {
                        'title': parsed.get('title', 'Learning Recommendation'),
                        'description': parsed.get('description', 'Personalized learning recommendation'),
                        'priority': parsed.get('priority', 'medium'),
                        'urgency': parsed.get('urgency', 'not_urgent'),
                        'confidence': 0.9,
                        'reasoning': parsed.get('reasoning', 'AI-generated recommendation'),
                        'action_items': parsed.get('action_items', [])
                    }
                except:
                    # Fallback if JSON parsing fails
                    return {
                        'title': 'Learning Recommendation',
                        'description': ai_content,
                        'priority': 'medium',
                        'urgency': 'not_urgent',
                        'confidence': 0.8,
                        'reasoning': 'AI-generated recommendation',
                        'action_items': ['Review the recommendation', 'Discuss with teacher']
                    }
            else:
                # Fallback recommendation
                return {
                    'title': 'Learning Recommendation',
                    'description': 'Consider reviewing recent lessons and practicing key concepts.',
                    'priority': 'medium',
                    'urgency': 'not_urgent',
                    'confidence': 0.7,
                    'reasoning': 'General learning recommendation',
                    'action_items': ['Review recent lessons', 'Practice key concepts', 'Ask questions when needed']
                }
                
        except Exception as e:
            # Fallback on error
            return {
                'title': 'Learning Recommendation',
                'description': 'Focus on consistent study habits and regular practice.',
                'priority': 'medium',
                'urgency': 'not_urgent',
                'confidence': 0.6,
                'reasoning': 'Fallback recommendation',
                'action_items': ['Maintain study schedule', 'Practice regularly', 'Seek help when needed']
            }


class AIBehavioralAnalysisListView(APIView):
    """
    List behavioral analysis data
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_student:
            analyses = AIBehavioralAnalysis.objects.filter(student=request.user)
        elif request.user.is_family:
            # Get analyses for family's students
            student_ids = request.user.family_students.values_list('id', flat=True)
            analyses = AIBehavioralAnalysis.objects.filter(student_id__in=student_ids)
        elif request.user.is_staff_member:
            # Staff can see analyses for students they're assigned to
            analyses = AIBehavioralAnalysis.objects.filter(
                student__in=request.user.assigned_students.all()
            )
        else:
            # Admin can see all analyses
            analyses = AIBehavioralAnalysis.objects.all()
        
        # Apply filters
        date_filter = request.query_params.get('date')
        if date_filter:
            analyses = analyses.filter(analysis_timestamp__date=date_filter)
        
        serializer = AIBehavioralAnalysisSerializer(analyses, many=True)
        return Response(serializer.data)


class AnalyzeBehaviorView(APIView):
    """
    Analyze student behavior from webcam data
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def post(self, request):
        # Check permissions
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can analyze behavior")
        
        student_id = request.data.get('student_id')
        session_id = request.data.get('session_id')
        frame_data = request.data.get('frame_data', {})
        
        if not student_id or not session_id:
            return Response({'error': 'Student ID and session ID are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = User.objects.get(id=student_id, role=User.UserRole.STUDENT)
            session = LearningSession.objects.get(id=session_id, student=student)
            
            # Analyze behavior using AI
            analysis_data = self.analyze_behavior(frame_data)
            
            # Create behavioral analysis record
            analysis = AIBehavioralAnalysis.objects.create(
                student=student,
                session=session,
                analysis_duration=analysis_data.get('duration', 0),
                attention_score=analysis_data.get('attention_score', 0),
                engagement_level=analysis_data.get('engagement_level', 'medium'),
                focus_quality=analysis_data.get('focus_quality', 'focused'),
                emotional_state=analysis_data.get('emotional_state', 'neutral'),
                emotional_confidence=analysis_data.get('emotional_confidence', 0),
                behavior_patterns=analysis_data.get('behavior_patterns', []),
                recommendations=analysis_data.get('recommendations', []),
                alerts=analysis_data.get('alerts', []),
                ai_model_used=analysis_data.get('model_used', 'fallback'),
                analysis_parameters=analysis_data.get('parameters', {}),
                analysis_quality_score=analysis_data.get('quality_score', 0)
            )
            
            serializer = AIBehavioralAnalysisSerializer(analysis)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        except LearningSession.DoesNotExist:
            return Response({'error': 'Learning session not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Failed to analyze behavior: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def analyze_behavior(self, frame_data):
        """Analyze behavior from frame data"""
        try:
            # This would integrate with computer vision models
            # For now, return mock analysis
            return {
                'duration': 30,
                'attention_score': 85.5,
                'engagement_level': 'high',
                'focus_quality': 'focused',
                'emotional_state': 'focused',
                'emotional_confidence': 0.8,
                'behavior_patterns': ['consistent attention', 'good posture'],
                'recommendations': ['Continue current engagement level'],
                'alerts': [],
                'model_used': 'opencv_analysis',
                'parameters': {'confidence_threshold': 0.7},
                'quality_score': 0.85
            }
        except Exception as e:
            # Fallback analysis
            return {
                'duration': 0,
                'attention_score': 50.0,
                'engagement_level': 'medium',
                'focus_quality': 'unknown',
                'emotional_state': 'neutral',
                'emotional_confidence': 0.5,
                'behavior_patterns': [],
                'recommendations': ['Analysis incomplete'],
                'alerts': ['Analysis failed'],
                'model_used': 'fallback',
                'parameters': {},
                'quality_score': 0.3
            }


class AIChatView(APIView):
    """
    General AI chat endpoint
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        message = request.data.get('message', '')
        context = request.data.get('context', '')
        
        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Generate AI response
            response = self.generate_chat_response(message, context, request.user)
            
            return Response({
                'message': message,
                'response': response['content'],
                'confidence': response['confidence'],
                'processing_time': response['processing_time']
            })
            
        except Exception as e:
            return Response({'error': f'Chat failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def generate_chat_response(self, message, context, user):
        """Generate AI chat response"""
        try:
            if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
                openai.api_key = settings.OPENAI_API_KEY
                
                # Build system prompt based on user role
                if user.is_student:
                    system_prompt = "You are a helpful AI teacher assistant for students. Provide educational, supportive, and age-appropriate responses."
                elif user.is_family:
                    system_prompt = "You are a helpful AI assistant for families. Provide guidance on supporting student learning and development."
                elif user.is_staff_member:
                    system_prompt = "You are a helpful AI assistant for teachers and staff. Provide educational insights and teaching support."
                else:
                    system_prompt = "You are a helpful AI assistant for the school management system."
                
                messages = [
                    {"role": "system", "content": system_prompt}
                ]
                
                if context:
                    messages.append({"role": "system", "content": f"Context: {context}"})
                
                messages.append({"role": "user", "content": message})
                
                start_time = timezone.now()
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=400,
                    temperature=0.7
                )
                end_time = timezone.now()
                
                processing_time = (end_time - start_time).total_seconds() * 1000
                
                return {
                    'content': response.choices[0].message.content,
                    'confidence': 0.9,
                    'processing_time': int(processing_time)
                }
            else:
                # Fallback response
                return {
                    'content': "I'm here to help! What would you like to know?",
                    'confidence': 0.7,
                    'processing_time': 100
                }
                
        except Exception as e:
            # Fallback on error
            return {
                'content': "I'm having trouble processing your request right now. Please try again later.",
                'confidence': 0.5,
                'processing_time': 0
            }


class SpeechToTextView(APIView):
    """
    Convert speech to text using AI
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        audio_file = request.FILES.get('audio')
        
        if not audio_file:
            return Response({'error': 'Audio file is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Save audio file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                for chunk in audio_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            # Convert speech to text
            text = self.speech_to_text(temp_file_path)
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            return Response({
                'text': text,
                'confidence': 0.9
            })
            
        except Exception as e:
            return Response({'error': f'Speech to text failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def speech_to_text(self, audio_file_path):
        """Convert speech to text using Whisper"""
        try:
            # Use Whisper for speech recognition
            model = whisper.load_model("base")
            result = model.transcribe(audio_file_path)
            return result["text"]
        except Exception as e:
            # Fallback to simple text
            return "Speech recognition failed"


class TextToSpeechView(APIView):
    """
    Convert text to speech using AI
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        text = request.data.get('text', '')
        language = request.data.get('language', 'en')
        
        if not text:
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Convert text to speech
            audio_data = self.text_to_speech(text, language)
            
            return Response({
                'audio_url': audio_data['url'],
                'duration': audio_data['duration']
            })
            
        except Exception as e:
            return Response({'error': f'Text to speech failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def text_to_speech(self, text, language):
        """Convert text to speech using gTTS"""
        try:
            # Use gTTS for text to speech
            tts = gtts.gTTS(text=text, lang=language, slow=False)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_file.name)
            
            # In production, you'd save this to a proper storage system
            # and return the URL
            return {
                'url': f'/media/audio/{temp_file.name}',
                'duration': len(text) / 150  # Rough estimate
            }
        except Exception as e:
            # Fallback
            return {
                'url': '/media/audio/fallback.mp3',
                'duration': 0
            }


# Additional view classes for CRUD operations
class AILessonUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        lesson = get_object_or_404(AILesson, pk=pk)
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can update lessons")
        
        serializer = AILessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AILessonDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        lesson = get_object_or_404(AILesson, pk=pk)
        if not (request.user.is_staff_member or request.user.is_admin):
            raise PermissionDenied("Only staff and administrators can delete lessons")
        
        lesson.is_active = False
        lesson.save()
        return Response({'message': 'Lesson deleted successfully'})


class EndConversationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        conversation = get_object_or_404(AIConversation, pk=pk)
        if not self.can_access_conversation(request.user, conversation):
            raise PermissionDenied("Access denied to this conversation")
        
        conversation.is_active = False
        conversation.status = 'completed'
        conversation.session_end = timezone.now()
        conversation.save()
        
        return Response({'message': 'Conversation ended successfully'})
    
    def can_access_conversation(self, user, conversation):
        if user.is_admin:
            return True
        if user.is_staff_member and conversation.student in user.assigned_students.all():
            return True
        if user.is_family and conversation.student in user.family_students.all():
            return True
        if user.is_student and conversation.student == user:
            return True
        return False


class MessageFeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        message = get_object_or_404(ConversationMessage, pk=pk)
        feedback = request.data.get('feedback')
        
        if feedback not in ['helpful', 'not_helpful', 'confusing', 'perfect']:
            return Response({'error': 'Invalid feedback type'}, status=status.HTTP_400_BAD_REQUEST)
        
        message.user_feedback = feedback
        message.save()
        
        return Response({'message': 'Feedback recorded successfully'})


class RecommendationFeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        recommendation = get_object_or_404(AIRecommendation, pk=pk)
        feedback = request.data.get('feedback')
        
        if feedback not in ['helpful', 'not_helpful', 'implemented', 'ignored']:
            return Response({'error': 'Invalid feedback type'}, status=status.HTTP_400_BAD_REQUEST)
        
        recommendation.student_feedback = feedback
        recommendation.save()
        
        return Response({'message': 'Feedback recorded successfully'})


# Placeholder views for remaining endpoints
class AIInsightsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'AI Insights endpoint - to be implemented'})


class StudentInsightsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, student_id):
        return Response({'message': f'Student insights for {student_id} - to be implemented'})


class ClassInsightsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, grade_level):
        return Response({'message': f'Class insights for {grade_level} - to be implemented'})


class AITeacherSettingsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'AI Teacher settings - to be implemented'})


class UpdateAISettingsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        return Response({'message': 'AI settings updated - to be implemented'})


class AIModelListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'AI models list - to be implemented'})


class AIModelDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, model_name):
        return Response({'message': f'AI model {model_name} details - to be implemented'})


class TestAIModelView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, model_name):
        return Response({'message': f'Testing AI model {model_name} - to be implemented'})


class GenerateLessonView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Lesson generation - to be implemented'})


# Phase 2: Advanced AI Features

class MultiLanguageView(APIView):
    """
    Multi-language support for Amharic, Oromo, and other local languages
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user's language preferences"""
        try:
            from .services import multi_language_service
            
            user = request.user
            language_pref, created = LanguagePreference.objects.get_or_create(user=user)
            
            return Response({
                'primary_language': language_pref.primary_language,
                'secondary_languages': language_pref.secondary_languages,
                'ai_response_language': language_pref.ai_response_language,
                'auto_translate': language_pref.auto_translate,
                'supported_languages': multi_language_service.SUPPORTED_LANGUAGES
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Update language preferences"""
        try:
            user = request.user
            language_pref, created = LanguagePreference.objects.get_or_create(user=user)
            
            language_pref.primary_language = request.data.get('primary_language', language_pref.primary_language)
            language_pref.secondary_languages = request.data.get('secondary_languages', language_pref.secondary_languages)
            language_pref.ai_response_language = request.data.get('ai_response_language', language_pref.ai_response_language)
            language_pref.auto_translate = request.data.get('auto_translate', language_pref.auto_translate)
            language_pref.save()
            
            return Response({'message': 'Language preferences updated successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TranslateContentView(APIView):
    """
    Translate content to different languages
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            from .services import multi_language_service
            
            text = request.data.get('text')
            target_language = request.data.get('target_language')
            source_language = request.data.get('source_language')
            
            if not text or not target_language:
                return Response({'error': 'Text and target_language are required'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            translated_text = multi_language_service.translate_text(
                text, target_language, source_language
            )
            
            return Response({
                'original_text': text,
                'translated_text': translated_text,
                'source_language': source_language or multi_language_service.detect_language(text),
                'target_language': target_language
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdvancedBehavioralAnalysisView(APIView):
    """
    Advanced computer vision behavioral analysis
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def post(self, request):
        try:
            from .services import computer_vision_service
            import cv2
            import numpy as np
            import base64
            
            # Handle different input formats
            if 'video_frame' in request.FILES:
                # File upload
                video_file = request.FILES['video_frame']
                # Convert to numpy array for processing
                file_bytes = video_file.read()
                nparr = np.frombuffer(file_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            elif 'frame_data' in request.data:
                # Base64 encoded frame
                frame_data = request.data['frame_data']
                if frame_data.startswith('data:image'):
                    frame_data = frame_data.split(',')[1]
                
                img_bytes = base64.b64decode(frame_data)
                nparr = np.frombuffer(img_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            else:
                return Response({'error': 'No video frame provided'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Analyze behavior
            analysis = computer_vision_service.analyze_student_behavior(frame)
            
            # Save analysis to database if student_id provided
            student_id = request.data.get('student_id')
            if student_id:
                try:
                    student = User.objects.get(id=student_id)
                    # Note: This would require a LearningSession object
                    # For now, we'll just return the analysis
                    pass
                except User.DoesNotExist:
                    pass
            
            return Response({
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PredictiveAnalyticsView(APIView):
    """
    AI-powered predictive analytics for learning outcomes
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            from .services import predictive_analytics_service
            
            student_id = request.data.get('student_id')
            if not student_id:
                return Response({'error': 'student_id is required'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Get student data
            try:
                student = User.objects.get(id=student_id)
            except User.DoesNotExist:
                return Response({'error': 'Student not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            # Prepare student data for prediction
            student_data = {
                'current_grade': request.data.get('current_grade', 85),
                'attendance_rate': request.data.get('attendance_rate', 90),
                'assignment_completion_rate': request.data.get('assignment_completion_rate', 88),
                'average_score': request.data.get('average_score', 82),
                'average_engagement_score': request.data.get('average_engagement_score', 75),
                'attention_score': request.data.get('attention_score', 78),
                'participation_rate': request.data.get('participation_rate', 80),
                'study_time_daily': request.data.get('study_time_daily', 120),
                'lesson_completion_rate': request.data.get('lesson_completion_rate', 85),
                'help_seeking_frequency': request.data.get('help_seeking_frequency', 3),
            }
            
            # Generate predictions
            predictions = predictive_analytics_service.predict_learning_outcomes(student_data)
            
            # Save to database
            analysis_type = request.data.get('analysis_type', 'academic_performance')
            prediction_horizon = request.data.get('prediction_horizon', '1_month')
            
            predictive_analysis = PredictiveAnalysis.objects.create(
                student=student,
                analysis_type=analysis_type,
                prediction_horizon=prediction_horizon,
                input_features=student_data,
                predictions=predictions,
                confidence_scores=predictions.get('confidence_intervals', {}),
                model_version='v1.0',
                recommended_actions=predictions.get('recommended_interventions', [])
            )
            
            return Response({
                'predictions': predictions,
                'analysis_id': predictive_analysis.id,
                'student_id': student_id,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NaturalLanguageUnderstandingView(APIView):
    """
    Enhanced Natural Language Understanding for better conversation context
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            from .services import nlu_service
            
            message = request.data.get('message')
            conversation_id = request.data.get('conversation_id')
            
            if not message:
                return Response({'error': 'message is required'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Get conversation history if conversation_id provided
            conversation_history = []
            if conversation_id:
                try:
                    conversation = AIConversation.objects.get(conversation_id=conversation_id)
                    messages = conversation.messages.order_by('sequence_number')
                    conversation_history = [
                        {
                            'role': msg.message_type,
                            'content': msg.content,
                            'timestamp': msg.timestamp.isoformat()
                        }
                        for msg in messages
                    ]
                except AIConversation.DoesNotExist:
                    pass
            
            # Analyze context
            context_analysis = nlu_service.analyze_conversation_context(
                conversation_history, message
            )
            
            return Response({
                'message': message,
                'context_analysis': context_analysis,
                'conversation_id': conversation_id,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Phase 3: Integration & Expansion

class OfflineCapabilitiesView(APIView):
    """
    Offline capabilities using local AI models
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get offline capabilities status"""
        try:
            from .offline_services import offline_ai_service
            
            connectivity = offline_ai_service.check_connectivity()
            statistics = offline_ai_service.get_offline_statistics()
            
            return Response({
                'connectivity': connectivity,
                'statistics': statistics,
                'offline_mode_available': True
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Generate offline AI response"""
        try:
            from .offline_services import offline_ai_service
            
            message = request.data.get('message')
            student_id = request.data.get('student_id')
            context = request.data.get('context', {})
            
            if not message:
                return Response({'error': 'message is required'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Generate offline response
            response_data = offline_ai_service.generate_offline_response(message, context)
            
            # Store interaction for later sync
            if student_id and 'response' in response_data:
                offline_ai_service.store_offline_interaction(
                    student_id, message, response_data['response']
                )
            
            return Response(response_data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OfflineSyncView(APIView):
    """
    Synchronize offline data when connection is restored
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            from .offline_services import offline_sync_service
            
            sync_results = offline_sync_service.sync_offline_data()
            
            return Response({
                'sync_results': sync_results,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CacheLessonOfflineView(APIView):
    """
    Cache lessons for offline access
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            from .offline_services import offline_ai_service
            
            lesson_id = request.data.get('lesson_id')
            if not lesson_id:
                return Response({'error': 'lesson_id is required'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            try:
                lesson = AILesson.objects.get(id=lesson_id)
            except AILesson.DoesNotExist:
                return Response({'error': 'Lesson not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            # Prepare lesson data for caching
            lesson_data = {
                'id': lesson.id,
                'title': lesson.title,
                'description': lesson.description,
                'content': lesson.content,
                'subject': lesson.subject,
                'grade_level': lesson.grade_level,
                'language': request.data.get('language', 'en')
            }
            
            # Cache lesson offline
            success = offline_ai_service.cache_lesson_offline(lesson_data)
            
            if success:
                return Response({'message': 'Lesson cached successfully for offline access'})
            else:
                return Response({'error': 'Failed to cache lesson'}, 
                              status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdvancedReportingView(APIView):
    """
    Advanced reporting and custom dashboard builder
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get available report types and dashboard widgets"""
        try:
            from analytics.dashboard_builder import dashboard_builder, report_generator
            
            return Response({
                'widget_types': dashboard_builder.WIDGET_TYPES,
                'chart_themes': dashboard_builder.CHART_THEMES,
                'report_types': report_generator.REPORT_TYPES
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Create custom dashboard or generate report"""
        try:
            from analytics.dashboard_builder import dashboard_builder, report_generator
            
            action = request.data.get('action')  # 'create_dashboard' or 'generate_report'
            
            if action == 'create_dashboard':
                dashboard_config = request.data.get('dashboard_config', {})
                dashboard = dashboard_builder.create_dashboard(dashboard_config)
                return Response(dashboard)
            
            elif action == 'generate_report':
                report_type = request.data.get('report_type')
                parameters = request.data.get('parameters', {})
                
                if not report_type:
                    return Response({'error': 'report_type is required'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                
                report = report_generator.generate_report(report_type, parameters)
                return Response(report)
            
            else:
                return Response({'error': 'Invalid action. Use "create_dashboard" or "generate_report"'}, 
                              status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
