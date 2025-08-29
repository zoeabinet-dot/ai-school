from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    # Lesson management
    path('', views.LessonListView.as_view(), name='lesson_list'),
    path('create/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    
    # Lesson plans
    path('<int:lesson_id>/plans/', views.LessonPlanListView.as_view(), name='lesson_plan_list'),
    
    # Lesson materials
    path('<int:lesson_id>/materials/', views.LessonMaterialListView.as_view(), name='lesson_material_list'),
    
    # Lesson assessments
    path('<int:lesson_id>/assessments/', views.LessonAssessmentListView.as_view(), name='lesson_assessment_list'),
    
    # Legacy endpoint for backward compatibility
    path('legacy/', views.lesson_list, name='lesson_list_legacy'),
]
