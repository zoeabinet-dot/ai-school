from django.db import models
from django.utils import timezone
from accounts.models import Student, User
from learning.models import Subject, Lesson


class AITeacherProfile(models.Model):
    """AI Teacher configuration and personality"""
    
    PERSONALITY_CHOICES = [
        ('encouraging', 'Encouraging and Supportive'),
        ('professional', 'Professional and Direct'),
        ('friendly', 'Friendly and Casual'),
        ('patient', 'Patient and Understanding'),
        ('enthusiastic', 'Enthusiastic and Energetic'),
    ]
    
    name = models.CharField(max_length=100, default='AI Teacher')
    personality_type = models.CharField(max_length=20, choices=PERSONALITY_CHOICES, default='encouraging')
    system_prompt = models.TextField()
    specializations = models.JSONField(default=list)  # Subject areas
    language_preferences = models.JSONField(default=list)
    voice_settings = models.JSONField(default=dict)  # Voice synthesis settings
    avatar_image = models.ImageField(upload_to='ai_avatars/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_personality_type_display()})"


class Conversation(models.Model):
    """AI conversations with students"""
    
    CONVERSATION_TYPE_CHOICES = [
        ('lesson_help', 'Lesson Help'),
        ('general_question', 'General Question'),
        ('homework_assistance', 'Homework Assistance'),
        ('motivation', 'Motivation and Encouragement'),
        ('explanation', 'Concept Explanation'),
        ('practice', 'Practice Session'),
        ('feedback', 'Feedback Discussion'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ai_conversations')
    ai_teacher = models.ForeignKey(AITeacherProfile, on_delete=models.CASCADE, related_name='conversations')
    conversation_type = models.CharField(max_length=20, choices=CONVERSATION_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    context = models.JSONField(default=dict)  # Additional context for the conversation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.get_conversation_type_display()}"


class Message(models.Model):
    """Individual messages in AI conversations"""
    
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text Message'),
        ('voice', 'Voice Message'),
        ('image', 'Image'),
        ('file', 'File Attachment'),
        ('system', 'System Message'),
    ]
    
    SENDER_CHOICES = [
        ('student', 'Student'),
        ('ai', 'AI Teacher'),
        ('system', 'System'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    content = models.TextField()
    metadata = models.JSONField(default=dict)  # Voice duration, file info, etc.
    attachments = models.JSONField(default=list)  # File paths/URLs
    is_flagged = models.BooleanField(default=False)  # For content moderation
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['conversation', 'timestamp']
    
    def __str__(self):
        return f"{self.conversation.id} - {self.sender} at {self.timestamp}"


class AIResponse(models.Model):
    """AI response generation tracking"""
    
    RESPONSE_TYPE_CHOICES = [
        ('text', 'Text Response'),
        ('voice', 'Voice Response'),
        ('mixed', 'Mixed Media Response'),
    ]
    
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='ai_response_data')
    prompt_tokens = models.IntegerField()
    completion_tokens = models.IntegerField()
    total_tokens = models.IntegerField()
    model_used = models.CharField(max_length=50)
    response_time_ms = models.IntegerField()
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    processing_metadata = models.JSONField(default=dict)
    
    def __str__(self):
        return f"AI Response for Message {self.message.id}"


class LearningRecommendation(models.Model):
    """AI-generated learning recommendations"""
    
    RECOMMENDATION_TYPE_CHOICES = [
        ('lesson', 'Lesson Recommendation'),
        ('practice', 'Practice Activity'),
        ('review', 'Review Material'),
        ('challenge', 'Challenge Problem'),
        ('resource', 'Additional Resource'),
        ('break', 'Take a Break'),
        ('help', 'Seek Help'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ai_recommendations')
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    reasoning = models.TextField()  # AI's reasoning for this recommendation
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    action_data = models.JSONField(default=dict)  # Specific action parameters
    is_accepted = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.title}"


class StudentAIInteraction(models.Model):
    """Track student interactions with AI for analytics"""
    
    INTERACTION_TYPE_CHOICES = [
        ('question_asked', 'Question Asked'),
        ('help_requested', 'Help Requested'),
        ('explanation_sought', 'Explanation Sought'),
        ('practice_started', 'Practice Started'),
        ('feedback_received', 'Feedback Received'),
        ('recommendation_viewed', 'Recommendation Viewed'),
        ('conversation_started', 'Conversation Started'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ai_interactions')
    interaction_type = models.CharField(max_length=30, choices=INTERACTION_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL, blank=True, null=True)
    duration_seconds = models.IntegerField(blank=True, null=True)
    satisfaction_rating = models.IntegerField(blank=True, null=True)  # 1-5 scale
    metadata = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.get_interaction_type_display()}"


class AITeachingSession(models.Model):
    """AI teaching sessions with students"""
    
    SESSION_TYPE_CHOICES = [
        ('individual_lesson', 'Individual Lesson'),
        ('practice_session', 'Practice Session'),
        ('review_session', 'Review Session'),
        ('assessment_prep', 'Assessment Preparation'),
        ('project_guidance', 'Project Guidance'),
        ('motivation_session', 'Motivation Session'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ai_teaching_sessions')
    ai_teacher = models.ForeignKey(AITeacherProfile, on_delete=models.CASCADE)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    objectives = models.JSONField(default=list)
    planned_activities = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    scheduled_start = models.DateTimeField()
    actual_start = models.DateTimeField(blank=True, null=True)
    actual_end = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    effectiveness_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    student_engagement_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.title}"


class AIFeedback(models.Model):
    """AI-generated feedback for students"""
    
    FEEDBACK_TYPE_CHOICES = [
        ('performance', 'Performance Feedback'),
        ('encouragement', 'Encouragement'),
        ('correction', 'Correction'),
        ('suggestion', 'Suggestion'),
        ('praise', 'Praise'),
        ('guidance', 'Guidance'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ai_feedback')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField()
    context = models.JSONField(default=dict)  # What triggered this feedback
    is_automated = models.BooleanField(default=True)
    is_read = models.BooleanField(default=False)
    is_helpful = models.BooleanField(blank=True, null=True)  # Student rating
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.get_feedback_type_display()}"