from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Learning Analytics
    path('learning/', views.LearningAnalyticsListView.as_view(), name='learning_analytics_list'),
    path('learning/create/', views.LearningAnalyticsCreateView.as_view(), name='learning_analytics_create'),
    path('learning/<int:pk>/', views.LearningAnalyticsDetailView.as_view(), name='learning_analytics_detail'),
    
    # Performance Metrics
    path('performance/', views.PerformanceMetricsListView.as_view(), name='performance_metrics_list'),
    path('performance/create/', views.PerformanceMetricsCreateView.as_view(), name='performance_metrics_create'),
    
    # Engagement Analytics
    path('engagement/', views.EngagementAnalyticsListView.as_view(), name='engagement_analytics_list'),
    
    # Dashboard Configuration
    path('dashboard-config/', views.DashboardConfigurationListView.as_view(), name='dashboard_config_list'),
    path('dashboard-config/create/', views.DashboardConfigurationCreateView.as_view(), name='dashboard_config_create'),
    path('dashboard-config/<int:pk>/update/', views.DashboardConfigurationUpdateView.as_view(), name='dashboard_config_update'),
    
    # Report Templates
    path('report-templates/', views.ReportTemplateListView.as_view(), name='report_template_list'),
    path('report-templates/create/', views.ReportTemplateCreateView.as_view(), name='report_template_create'),
    
    # Student Analytics Dashboard
    path('student/<int:student_id>/dashboard/', views.StudentAnalyticsDashboardView.as_view(), name='student_analytics_dashboard'),
    
    # Class Analytics
    path('class/<str:grade_level>/', views.ClassAnalyticsView.as_view(), name='class_analytics'),
    
    # Analytics Export
    path('export/', views.AnalyticsExportView.as_view(), name='analytics_export'),
    
    # Analytics Insights
    path('insights/', views.AnalyticsInsightsView.as_view(), name='analytics_insights'),
    
    # Legacy endpoint for backward compatibility
    path('legacy/', views.analytics_list, name='analytics_list_legacy'),
]