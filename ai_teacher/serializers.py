from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    AILesson, AIConversation, ConversationMessage, 
    AIRecommendation, AIBehavioralAnalysis
)

User = get_user_model()


class AILessonSerializer(serializers.ModelSerializer):
    """
    Serializer for AI Lesson model
    """
    created_by = serializers.ReadOnlyField(source='created_by.username')
    subject_display = serializers.CharField(source='get_subject_display', read_only=True)
    grade_level_display = serializers.CharField(source='get_grade_level_display', read_only=True)
    difficulty_level_display = serializers.CharField(source='get_difficulty_level_display', read_only=True)
    lesson_type_display = serializers.CharField(source='get_lesson_type_display', read_only=True)
    
    class Meta:
        model = AILesson
        fields = [
            'id', 'title', 'description', 'subject', 'subject_display',
            'grade_level', 'grade_level_display', 'difficulty_level', 'difficulty_level_display',
            'lesson_type', 'lesson_type_display', 'content', 'learning_objectives',
            'prerequisites', 'ai_model_used', 'ai_generation_prompt', 'ai_parameters',
            'estimated_duration', 'is_adaptive', 'is_active', 'tags', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class AILessonCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating AI lessons
    """
    class Meta:
        model = AILesson
        fields = [
            'title', 'description', 'subject', 'grade_level', 'difficulty_level',
            'lesson_type', 'content', 'learning_objectives', 'prerequisites',
            'estimated_duration', 'is_adaptive', 'tags'
        ]
    
    def validate_content(self, value):
        """Validate lesson content structure"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Content must be a valid JSON object")
        return value
    
    def validate_learning_objectives(self, value):
        """Validate learning objectives"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Learning objectives must be a list")
        return value


class AIConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for AI Conversation model
    """
    student = serializers.ReadOnlyField(source='student.username')
    student_name = serializers.ReadOnlyField(source='student.get_full_name')
    lesson_title = serializers.ReadOnlyField(source='lesson.title')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AIConversation
        fields = [
            'id', 'student', 'student_name', 'lesson', 'lesson_title',
            'conversation_id', 'session_start', 'session_end', 'context',
            'learning_objectives', 'ai_model', 'ai_personality', 'is_active',
            'status', 'status_display', 'message_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'conversation_id', 'session_start', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        """Get count of messages in conversation"""
        return obj.messages.count()


class AIConversationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating AI conversations
    """
    class Meta:
        model = AIConversation
        fields = [
            'lesson', 'context', 'learning_objectives', 'ai_model', 'ai_personality'
        ]
    
    def validate_context(self, value):
        """Validate conversation context"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Context must be a valid JSON object")
        return value


class ConversationMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation Message model
    """
    conversation = serializers.ReadOnlyField(source='conversation.id')
    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    user_feedback_display = serializers.CharField(source='get_user_feedback_display', read_only=True)
    
    class Meta:
        model = ConversationMessage
        fields = [
            'id', 'conversation', 'content', 'message_type', 'message_type_display',
            'timestamp', 'sequence_number', 'ai_model_response', 'ai_confidence',
            'user_feedback', 'user_feedback_display', 'processing_time_ms',
            'tokens_used'
        ]
        read_only_fields = ['id', 'timestamp', 'sequence_number']


class ConversationMessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating conversation messages
    """
    class Meta:
        model = ConversationMessage
        fields = ['content', 'message_type']
    
    def validate_message_type(self, value):
        """Validate message type"""
        valid_types = ['user', 'ai', 'system', 'instruction']
        if value not in valid_types:
            raise serializers.ValidationError(f"Invalid message type. Must be one of: {valid_types}")
        return value


class AIRecommendationSerializer(serializers.ModelSerializer):
    """
    Serializer for AI Recommendation model
    """
    student = serializers.ReadOnlyField(source='student.username')
    student_name = serializers.ReadOnlyField(source='student.get_full_name')
    recommendation_type_display = serializers.CharField(source='get_recommendation_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    urgency_display = serializers.CharField(source='get_urgency_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    student_feedback_display = serializers.CharField(source='get_student_feedback_display', read_only=True)
    estimated_effort_display = serializers.CharField(source='get_estimated_effort_display', read_only=True)
    
    class Meta:
        model = AIRecommendation
        fields = [
            'id', 'student', 'student_name', 'title', 'description',
            'recommendation_type', 'recommendation_type_display', 'priority',
            'priority_display', 'urgency', 'urgency_display', 'ai_confidence',
            'reasoning', 'supporting_data', 'action_items', 'estimated_effort',
            'estimated_effort_display', 'status', 'status_display',
            'student_feedback', 'student_feedback_display', 'created_at',
            'updated_at', 'expires_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AIRecommendationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating AI recommendations
    """
    class Meta:
        model = AIRecommendation
        fields = [
            'student', 'title', 'description', 'recommendation_type',
            'priority', 'urgency', 'ai_confidence', 'reasoning',
            'supporting_data', 'action_items', 'estimated_effort'
        ]
    
    def validate_ai_confidence(self, value):
        """Validate AI confidence score"""
        if value < 0 or value > 100:
            raise serializers.ValidationError("AI confidence must be between 0 and 100")
        return value
    
    def validate_action_items(self, value):
        """Validate action items"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Action items must be a list")
        return value


class AIBehavioralAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for AI Behavioral Analysis model
    """
    student = serializers.ReadOnlyField(source='student.username')
    student_name = serializers.ReadOnlyField(source='student.get_full_name')
    session = serializers.ReadOnlyField(source='session.id')
    engagement_level_display = serializers.CharField(source='get_engagement_level_display', read_only=True)
    focus_quality_display = serializers.CharField(source='get_focus_quality_display', read_only=True)
    emotional_state_display = serializers.CharField(source='get_emotional_state_display', read_only=True)
    
    class Meta:
        model = AIBehavioralAnalysis
        fields = [
            'id', 'student', 'student_name', 'session', 'analysis_timestamp',
            'analysis_duration', 'attention_score', 'engagement_level',
            'engagement_level_display', 'focus_quality', 'focus_quality_display',
            'emotional_state', 'emotional_state_display', 'emotional_confidence',
            'behavior_patterns', 'recommendations', 'alerts', 'ai_model_used',
            'analysis_parameters', 'analysis_quality_score', 'created_at'
        ]
        read_only_fields = ['id', 'analysis_timestamp', 'created_at']


class AIBehavioralAnalysisCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating behavioral analysis
    """
    class Meta:
        model = AIBehavioralAnalysis
        fields = [
            'student', 'session', 'analysis_duration', 'attention_score',
            'engagement_level', 'focus_quality', 'emotional_state',
            'emotional_confidence', 'behavior_patterns', 'recommendations',
            'alerts', 'ai_model_used', 'analysis_parameters',
            'analysis_quality_score'
        ]
    
    def validate_attention_score(self, value):
        """Validate attention score"""
        if value < 0 or value > 100:
            raise serializers.ValidationError("Attention score must be between 0 and 100")
        return value
    
    def validate_emotional_confidence(self, value):
        """Validate emotional confidence"""
        if value and (value < 0 or value > 100):
            raise serializers.ValidationError("Emotional confidence must be between 0 and 100")
        return value


class AIChatSerializer(serializers.Serializer):
    """
    Serializer for AI chat requests
    """
    message = serializers.CharField(max_length=1000, required=True)
    context = serializers.CharField(max_length=500, required=False, allow_blank=True)
    conversation_id = serializers.CharField(max_length=100, required=False, allow_blank=True)


class AIChatResponseSerializer(serializers.Serializer):
    """
    Serializer for AI chat responses
    """
    message = serializers.CharField()
    response = serializers.CharField()
    confidence = serializers.FloatField()
    processing_time = serializers.IntegerField()
    conversation_id = serializers.CharField(required=False)


class SpeechToTextSerializer(serializers.Serializer):
    """
    Serializer for speech to text requests
    """
    audio = serializers.FileField(required=True)
    language = serializers.CharField(max_length=10, default='en')
    model = serializers.CharField(max_length=50, default='base')


class SpeechToTextResponseSerializer(serializers.Serializer):
    """
    Serializer for speech to text responses
    """
    text = serializers.CharField()
    confidence = serializers.FloatField()
    language = serializers.CharField()
    processing_time = serializers.FloatField()


class TextToSpeechSerializer(serializers.Serializer):
    """
    Serializer for text to speech requests
    """
    text = serializers.CharField(max_length=1000, required=True)
    language = serializers.CharField(max_length=10, default='en')
    speed = serializers.ChoiceField(choices=[('slow', 'Slow'), ('normal', 'Normal'), ('fast', 'Fast')], default='normal')
    voice = serializers.CharField(max_length=50, required=False, allow_blank=True)


class TextToSpeechResponseSerializer(serializers.Serializer):
    """
    Serializer for text to speech responses
    """
    audio_url = serializers.CharField()
    duration = serializers.FloatField()
    language = serializers.CharField()
    text_length = serializers.IntegerField()


class LessonGenerationSerializer(serializers.Serializer):
    """
    Serializer for lesson generation requests
    """
    subject = serializers.CharField(max_length=100, required=True)
    grade_level = serializers.CharField(max_length=20, required=True)
    difficulty_level = serializers.CharField(max_length=20, required=True)
    lesson_type = serializers.CharField(max_length=50, required=True)
    learning_objectives = serializers.ListField(child=serializers.CharField(), required=False)
    estimated_duration = serializers.IntegerField(min_value=5, max_value=120, required=True)
    ai_model = serializers.CharField(max_length=100, default='gpt-4')
    custom_prompt = serializers.CharField(max_length=1000, required=False, allow_blank=True)


class LessonGenerationResponseSerializer(serializers.Serializer):
    """
    Serializer for lesson generation responses
    """
    lesson = AILessonSerializer()
    generation_time = serializers.FloatField()
    ai_model_used = serializers.CharField()
    confidence_score = serializers.FloatField()
    suggestions = serializers.ListField(child=serializers.CharField())


class BehaviorAnalysisRequestSerializer(serializers.Serializer):
    """
    Serializer for behavior analysis requests
    """
    student_id = serializers.IntegerField(required=True)
    session_id = serializers.IntegerField(required=True)
    frame_data = serializers.JSONField(required=True)
    analysis_type = serializers.ChoiceField(
        choices=['attention', 'engagement', 'emotion', 'comprehensive'],
        default='comprehensive'
    )
    ai_model = serializers.CharField(max_length=100, default='opencv_analysis')


class BehaviorAnalysisResponseSerializer(serializers.Serializer):
    """
    Serializer for behavior analysis responses
    """
    analysis = AIBehavioralAnalysisSerializer()
    processing_time = serializers.FloatField()
    model_used = serializers.CharField()
    quality_score = serializers.FloatField()
    alerts = serializers.ListField(child=serializers.CharField())


class RecommendationGenerationSerializer(serializers.Serializer):
    """
    Serializer for recommendation generation requests
    """
    student_id = serializers.IntegerField(required=True)
    recommendation_type = serializers.CharField(max_length=50, required=True)
    context = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    priority_level = serializers.ChoiceField(
        choices=['low', 'medium', 'high', 'urgent'],
        default='medium'
    )
    ai_model = serializers.CharField(max_length=100, default='gpt-4')


class RecommendationGenerationResponseSerializer(serializers.Serializer):
    """
    Serializer for recommendation generation responses
    """
    recommendation = AIRecommendationSerializer()
    generation_time = serializers.FloatField()
    ai_model_used = serializers.CharField()
    confidence_score = serializers.FloatField()
    reasoning_summary = serializers.CharField()


class AILessonFilterSerializer(serializers.Serializer):
    """
    Serializer for AI lesson filtering
    """
    subject = serializers.CharField(max_length=100, required=False, allow_blank=True)
    grade_level = serializers.CharField(max_length=20, required=False, allow_blank=True)
    difficulty_level = serializers.CharField(max_length=20, required=False, allow_blank=True)
    lesson_type = serializers.CharField(max_length=50, required=False, allow_blank=True)
    is_adaptive = serializers.BooleanField(required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    created_after = serializers.DateField(required=False)
    created_before = serializers.DateField(required=False)


class ConversationFilterSerializer(serializers.Serializer):
    """
    Serializer for conversation filtering
    """
    student_id = serializers.IntegerField(required=False)
    lesson_id = serializers.IntegerField(required=False)
    status = serializers.CharField(max_length=20, required=False, allow_blank=True)
    ai_model = serializers.CharField(max_length=100, required=False, allow_blank=True)
    session_start_after = serializers.DateTimeField(required=False)
    session_start_before = serializers.DateTimeField(required=False)


class RecommendationFilterSerializer(serializers.Serializer):
    """
    Serializer for recommendation filtering
    """
    student_id = serializers.IntegerField(required=False)
    recommendation_type = serializers.CharField(max_length=50, required=False, allow_blank=True)
    priority = serializers.CharField(max_length=20, required=False, allow_blank=True)
    urgency = serializers.CharField(max_length=20, required=False, allow_blank=True)
    status = serializers.CharField(max_length=20, required=False, allow_blank=True)
    created_after = serializers.DateField(required=False)
    created_before = serializers.DateField(required=False)


class BehavioralAnalysisFilterSerializer(serializers.Serializer):
    """
    Serializer for behavioral analysis filtering
    """
    student_id = serializers.IntegerField(required=False)
    session_id = serializers.IntegerField(required=False)
    engagement_level = serializers.CharField(max_length=20, required=False, allow_blank=True)
    focus_quality = serializers.CharField(max_length=50, required=False, allow_blank=True)
    emotional_state = serializers.CharField(max_length=50, required=False, allow_blank=True)
    analysis_after = serializers.DateTimeField(required=False)
    analysis_before = serializers.DateTimeField(required=False)
    ai_model = serializers.CharField(max_length=100, required=False, allow_blank=True)


class AITeacherSettingsSerializer(serializers.Serializer):
    """
    Serializer for AI teacher settings
    """
    default_ai_model = serializers.CharField(max_length=100, default='gpt-4')
    conversation_memory_limit = serializers.IntegerField(min_value=5, max_value=50, default=20)
    max_response_tokens = serializers.IntegerField(min_value=100, max_value=2000, default=500)
    temperature = serializers.FloatField(min_value=0.0, max_value=2.0, default=0.7)
    enable_voice_features = serializers.BooleanField(default=True)
    enable_behavioral_analysis = serializers.BooleanField(default=True)
    privacy_level = serializers.ChoiceField(
        choices=['minimal', 'partial', 'full'],
        default='partial'
    )
    auto_generate_recommendations = serializers.BooleanField(default=True)
    recommendation_frequency = serializers.ChoiceField(
        choices=['daily', 'weekly', 'monthly'],
        default='weekly'
    )