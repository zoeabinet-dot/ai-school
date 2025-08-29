from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    # Webcam Sessions
    path('sessions/', views.WebcamSessionListView.as_view(), name='session_list'),
    path('sessions/create/', views.WebcamSessionCreateView.as_view(), name='session_create'),
    path('sessions/<int:pk>/', views.WebcamSessionDetailView.as_view(), name='session_detail'),
    path('sessions/<int:pk>/end/', views.WebcamSessionEndView.as_view(), name='session_end'),
    
    # Frame Analysis
    path('sessions/<int:session_id>/frames/', views.FrameAnalysisListView.as_view(), name='frame_analysis_list'),
    path('sessions/<int:session_id>/frames/create/', views.FrameAnalysisCreateView.as_view(), name='frame_analysis_create'),
    
    # Behavior Events
    path('events/', views.BehaviorEventListView.as_view(), name='behavior_event_list'),
    path('events/create/', views.BehaviorEventCreateView.as_view(), name='behavior_event_create'),
    
    # Privacy Settings
    path('privacy/', views.PrivacySettingsListView.as_view(), name='privacy_settings_list'),
    path('privacy/create/', views.PrivacySettingsCreateView.as_view(), name='privacy_settings_create'),
    path('privacy/<int:pk>/update/', views.PrivacySettingsUpdateView.as_view(), name='privacy_settings_update'),
    
    # Monitoring Alerts
    path('alerts/', views.MonitoringAlertListView.as_view(), name='alert_list'),
    path('alerts/create/', views.MonitoringAlertCreateView.as_view(), name='alert_create'),
    path('alerts/<int:pk>/update/', views.MonitoringAlertUpdateView.as_view(), name='alert_update'),
    
    # Student Monitoring Dashboard
    path('student/<int:student_id>/dashboard/', views.StudentMonitoringDashboardView.as_view(), name='student_monitoring_dashboard'),
    
    # Real-time Monitoring
    path('realtime/<int:session_id>/', views.RealTimeMonitoringView.as_view(), name='realtime_monitoring'),
    
    # Behavior Analysis
    path('behavior-analysis/', views.BehaviorAnalysisView.as_view(), name='behavior_analysis'),
    
    # Privacy Compliance
    path('compliance/', views.PrivacyComplianceView.as_view(), name='privacy_compliance'),
    
    # Legacy endpoint for backward compatibility
    path('legacy/', views.monitoring_list, name='monitoring_list_legacy'),
]