from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'webcam_monitoring'

router = DefaultRouter()
router.register(r'sessions', views.WebcamSessionViewSet, basename='session')
router.register(r'alerts', views.AlertEventViewSet, basename='alert')
router.register(r'reports', views.MonitoringReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
    path('start-session/', views.StartMonitoringView.as_view(), name='start_session'),
    path('end-session/', views.EndMonitoringView.as_view(), name='end_session'),
    path('analyze-frame/', views.AnalyzeFrameView.as_view(), name='analyze_frame'),
    path('settings/', views.MonitoringSettingsView.as_view(), name='settings'),
    path('consent/', views.ConsentView.as_view(), name='consent'),
]