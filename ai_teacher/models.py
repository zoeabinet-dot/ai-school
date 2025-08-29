from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class AILesson(models.Model):
    """
    AI-generated and managed lessons for students
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Lesson metadata
    subject = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=20, choices=[
        ('K', 'Kindergarten'),
        ('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3'),
        ('4', 'Grade 4'), ('5', 'Grade 5'), ('6', 'Grade 6'),
        ('7', 'Grade 7'), ('8', 'Grade 8'), ('9', 'Grade 9'),
        ('10', 'Grade 10'), ('11', 'Grade 11'), ('12', 'Grade 12'),
    ])
    
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ])
    
    lesson_type = models.CharField(max_length=50, choices=[
        ('interactive', 'Interactive AI'),
        ('video', 'Video Lesson'),
        ('reading', 'Reading Material'),
        ('quiz', 'Quiz/Assessment'),
        ('project', 'Project-Based'),
        ('practice', 'Practice Exercise'),
    ])
    
    # Content and structure
    content = models.JSONField(default=dict, help_text="Structured lesson content")
    learning_objectives = models.JSONField(default=list)
    prerequisites = models.JSONField(default=list)
    
    # AI generation details
    ai_model_used = models.CharField(max_length=100, blank=True, null=True)
    ai_generation_prompt = models.TextField(blank=True, null=True)
    ai_parameters = models.JSONField(default=dict, blank=True)
    
    # Lesson settings
    estimated_duration = models.IntegerField(help_text="Duration in minutes")
    is_adaptive = models.BooleanField(default=True, help_text="AI can modify lesson based on student performance")
    is_active = models.BooleanField(default=True)
    
    # Metadata
    tags = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='created_lessons'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_lessons'
        ordering = ['subject', 'grade_level', 'difficulty_level']
    
    def __str__(self):
        return f"{self.title} - {self.subject} Grade {self.grade_level}"


class AIConversation(models.Model):
    """
    AI Teacher conversations with students
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_conversations')
    lesson = models.ForeignKey(AILesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    
    # Conversation metadata
    conversation_id = models.CharField(max_length=100, unique=True)
    session_start = models.DateTimeField(auto_now_add=True)
    session_end = models.DateTimeField(blank=True, null=True)
    
    # Conversation context
    context = models.JSONField(default=dict, help_text="Conversation context and memory")
    learning_objectives = models.JSONField(default=list)
    
    # AI model information
    ai_model = models.CharField(max_length=100, default='gpt-4')
    ai_personality = models.CharField(max_length=100, default='helpful_teacher')
    
    # Conversation status
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ], default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_conversations'
        ordering = ['-session_start']
    
    def __str__(self):
        return f"AI Conversation with {self.student.get_full_name()} - {self.conversation_id}"


class ConversationMessage(models.Model):
    """
    Individual messages in AI conversations
    """
    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name='messages')
    
    # Message content
    content = models.TextField()
    message_type = models.CharField(max_length=20, choices=[
        ('user', 'User Message'),
        ('ai', 'AI Response'),
        ('system', 'System Message'),
        ('instruction', 'Instruction'),
    ])
    
    # Message metadata
    timestamp = models.DateTimeField(auto_now_add=True)
    sequence_number = models.IntegerField()
    
    # AI-specific fields
    ai_model_response = models.JSONField(default=dict, blank=True)
    ai_confidence = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    # User interaction
    user_feedback = models.CharField(max_length=20, choices=[
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('confusing', 'Confusing'),
        ('perfect', 'Perfect'),
    ], blank=True, null=True)
    
    # Processing information
    processing_time_ms = models.IntegerField(blank=True, null=True)
    tokens_used = models.IntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'conversation_messages'
        ordering = ['conversation', 'sequence_number']
        unique_together = ['conversation', 'sequence_number']
    
    def __str__(self):
        return f"Message {self.sequence_number} in {self.conversation.conversation_id}"


class AIRecommendation(models.Model):
    """
    AI-generated recommendations for students
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_recommendations')
    
    # Recommendation details
    title = models.CharField(max_length=200)
    description = models.TextField()
    recommendation_type = models.CharField(max_length=50, choices=[
        ('lesson', 'Lesson Recommendation'),
        ('study_plan', 'Study Plan'),
        ('resource', 'Learning Resource'),
        ('activity', 'Activity Suggestion'),
        ('goal', 'Goal Setting'),
        ('behavior', 'Behavioral'),
        ('social', 'Social Development'),
    ])
    
    # Priority and urgency
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='medium')
    
    urgency = models.CharField(max_length=20, choices=[
        ('not_urgent', 'Not Urgent'),
        ('soon', 'Soon'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical'),
    ], default='not_urgent')
    
    # AI analysis
    ai_confidence = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    reasoning = models.TextField(help_text="AI explanation for this recommendation")
    supporting_data = models.JSONField(default=dict, blank=True)
    
    # Implementation
    action_items = models.JSONField(default=list, blank=True)
    estimated_effort = models.CharField(max_length=20, choices=[
        ('low', 'Low Effort'),
        ('medium', 'Medium Effort'),
        ('high', 'High Effort'),
    ], blank=True, null=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('dismissed', 'Dismissed'),
        ('expired', 'Expired'),
    ], default='pending')
    
    # Feedback
    student_feedback = models.CharField(max_length=20, choices=[
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('implemented', 'Implemented'),
        ('ignored', 'Ignored'),
    ], blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'ai_recommendations'
        ordering = ['-priority', '-urgency', '-created_at']
    
    def __str__(self):
        return f"{self.title} for {self.student.get_full_name()}"


class AIBehavioralAnalysis(models.Model):
    """
    AI analysis of student behavior and engagement
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='behavioral_analyses')
    session = models.ForeignKey('students.LearningSession', on_delete=models.CASCADE, related_name='behavioral_analyses')
    
    # Analysis metadata
    analysis_timestamp = models.DateTimeField(auto_now_add=True)
    analysis_duration = models.IntegerField(help_text="Duration of analysis in seconds")
    
    # Behavioral metrics
    attention_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    engagement_level = models.CharField(max_length=20, choices=[
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ])
    
    focus_quality = models.CharField(max_length=20, choices=[
        ('distracted', 'Distracted'),
        ('partially_focused', 'Partially Focused'),
        ('focused', 'Focused'),
        ('highly_focused', 'Highly Focused'),
    ])
    
    # Emotional analysis
    emotional_state = models.CharField(max_length=50, choices=[
        ('happy', 'Happy'),
        ('focused', 'Focused'),
        ('frustrated', 'Frustrated'),
        ('bored', 'Bored'),
        ('confused', 'Confused'),
        ('excited', 'Excited'),
        ('neutral', 'Neutral'),
    ], blank=True, null=True)
    
    emotional_confidence = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    # AI insights
    behavior_patterns = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    alerts = models.JSONField(default=list, blank=True)
    
    # Technical details
    ai_model_used = models.CharField(max_length=100)
    analysis_parameters = models.JSONField(default=dict, blank=True)
    
    # Quality metrics
    analysis_quality_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_behavioral_analyses'
        ordering = ['-analysis_timestamp']
    
    def __str__(self):
        return f"Behavioral Analysis for {self.student.get_full_name()} at {self.analysis_timestamp}"
