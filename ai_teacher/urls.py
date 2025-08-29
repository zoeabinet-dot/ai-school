from django.urls import path, include
from . import views

app_name = 'ai_teacher'

urlpatterns = [
    # AI Lessons
    path('lessons/', views.AILessonListView.as_view(), name='lesson_list'),
    path('lessons/create/', views.AILessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/', views.AILessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/update/', views.AILessonUpdateView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', views.AILessonDeleteView.as_view(), name='lesson_delete'),
    
    # AI Conversations
    path('conversations/', views.AIConversationListView.as_view(), name='conversation_list'),
    path('conversations/create/', views.AIConversationCreateView.as_view(), name='conversation_create'),
    path('conversations/<int:pk>/', views.AIConversationDetailView.as_view(), name='conversation_detail'),
    path('conversations/<int:pk>/messages/', views.ConversationMessageListView.as_view(), name='conversation_messages'),
    path('conversations/<int:pk>/send-message/', views.SendMessageView.as_view(), name='send_message'),
    path('conversations/<int:pk>/end/', views.EndConversationView.as_view(), name='end_conversation'),
    
    # Conversation Messages
    path('messages/', views.ConversationMessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/feedback/', views.MessageFeedbackView.as_view(), name='message_feedback'),
    
    # AI Recommendations
    path('recommendations/', views.AIRecommendationListView.as_view(), name='recommendation_list'),
    path('recommendations/<int:pk>/feedback/', views.RecommendationFeedbackView.as_view(), name='recommendation_feedback'),
    
    # Behavioral Analysis
    path('behavioral-analysis/', views.AIBehavioralAnalysisListView.as_view(), name='behavioral_analysis_list'),
    
    # AI Services
    path('generate-lesson/', views.GenerateLessonView.as_view(), name='generate_lesson'),
    path('analyze-behavior/', views.AnalyzeBehaviorView.as_view(), name='analyze_behavior'),
    path('generate-recommendation/', views.GenerateRecommendationView.as_view(), name='generate_recommendation'),
    path('chat/', views.AIChatView.as_view(), name='ai_chat'),
    
    # Voice and Speech
    path('speech-to-text/', views.SpeechToTextView.as_view(), name='speech_to_text'),
    path('text-to-speech/', views.TextToSpeechView.as_view(), name='text_to_speech'),
    
    # AI Model Management
    path('models/', views.AIModelListView.as_view(), name='ai_model_list'),
    path('models/<str:model_name>/', views.AIModelDetailView.as_view(), name='ai_model_detail'),
    path('models/<str:model_name>/test/', views.TestAIModelView.as_view(), name='test_ai_model'),
    
    # Analytics and Insights
    path('insights/', views.AIInsightsView.as_view(), name='ai_insights'),
    path('insights/student/<int:student_id>/', views.StudentInsightsView.as_view(), name='student_insights'),
    path('insights/class/<str:grade_level>/', views.ClassInsightsView.as_view(), name='class_insights'),
    
    # Settings and Configuration
    path('settings/', views.AITeacherSettingsView.as_view(), name='ai_teacher_settings'),
    path('settings/update/', views.UpdateAISettingsView.as_view(), name='update_ai_settings'),
]