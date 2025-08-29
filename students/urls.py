from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Student management
    path('', views.StudentListView.as_view(), name='student_list'),
    path('create/', views.StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('search/', views.StudentSearchView.as_view(), name='student_search'),
    
    # Academic records
    path('<int:student_id>/academic-records/', views.AcademicRecordListView.as_view(), name='academic_record_list'),
    path('<int:student_id>/academic-records/create/', views.AcademicRecordCreateView.as_view(), name='academic_record_create'),
    
    # Student projects
    path('<int:student_id>/projects/', views.StudentProjectListView.as_view(), name='project_list'),
    path('<int:student_id>/projects/create/', views.StudentProjectCreateView.as_view(), name='project_create'),
    
    # Learning sessions
    path('<int:student_id>/sessions/', views.LearningSessionListView.as_view(), name='session_list'),
    path('<int:student_id>/sessions/create/', views.LearningSessionCreateView.as_view(), name='session_create'),
    path('sessions/<int:session_id>/end/', views.LearningSessionEndView.as_view(), name='session_end'),
    
    # Student goals
    path('<int:student_id>/goals/', views.StudentGoalListView.as_view(), name='goal_list'),
    path('<int:student_id>/goals/create/', views.StudentGoalCreateView.as_view(), name='goal_create'),
    path('goals/<int:goal_id>/update/', views.StudentGoalUpdateView.as_view(), name='goal_update'),
    
    # Dashboard and reports
    path('<int:student_id>/dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    
    # Legacy endpoint for backward compatibility
    path('legacy/', views.student_list, name='student_list_legacy'),
]