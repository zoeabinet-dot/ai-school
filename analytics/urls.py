from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'analytics'

router = DefaultRouter()
router.register(r'performance', views.StudentPerformanceViewSet, basename='performance')
router.register(r'attendance', views.AttendanceViewSet, basename='attendance')
router.register(r'engagement', views.EngagementViewSet, basename='engagement')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    path('reports/student/<int:student_id>/', views.StudentReportView.as_view(), name='student_report'),
    path('reports/classroom/', views.ClassroomReportView.as_view(), name='classroom_report'),
    path('insights/', views.LearningInsightsView.as_view(), name='learning_insights'),
]