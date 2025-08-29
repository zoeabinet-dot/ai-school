from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'learning'

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r'learning-paths', views.LearningPathViewSet, basename='learningpath')
router.register(r'lessons', views.LessonViewSet, basename='lesson')
router.register(r'assignments', views.AssignmentViewSet, basename='assignment')
router.register(r'quizzes', views.QuizViewSet, basename='quiz')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'portfolio', views.StudentPortfolioViewSet, basename='studentportfolio')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Custom endpoints
    path('progress/', views.LearningProgressView.as_view(), name='learning_progress'),
    path('progress/<int:student_id>/', views.StudentProgressView.as_view(), name='student_progress'),
    path('lessons/<int:lesson_id>/progress/', views.LessonProgressView.as_view(), name='lesson_progress'),
    path('assignments/<int:assignment_id>/submit/', views.AssignmentSubmissionView.as_view(), name='assignment_submit'),
    path('assignments/<int:assignment_id>/submissions/', views.AssignmentSubmissionListView.as_view(), name='assignment_submissions'),
    path('quizzes/<int:quiz_id>/attempt/', views.QuizAttemptView.as_view(), name='quiz_attempt'),
    path('quizzes/<int:quiz_id>/attempts/', views.QuizAttemptListView.as_view(), name='quiz_attempts'),
    path('student-dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('teacher-dashboard/', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
]