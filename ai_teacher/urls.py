from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'ai_teacher'

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'recommendations', views.LearningRecommendationViewSet, basename='recommendation')
router.register(r'feedback', views.AIFeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
    path('chat/', views.AIChatView.as_view(), name='ai_chat'),
    path('voice-chat/', views.VoiceChatView.as_view(), name='voice_chat'),
    path('generate-lesson/', views.GenerateLessonView.as_view(), name='generate_lesson'),
    path('analyze-performance/', views.AnalyzePerformanceView.as_view(), name='analyze_performance'),
    path('teaching-sessions/', views.AITeachingSessionView.as_view(), name='teaching_sessions'),
]