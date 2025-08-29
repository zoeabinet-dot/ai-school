from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('student-dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('family-dashboard/', views.FamilyDashboardView.as_view(), name='family_dashboard'),
    path('staff-dashboard/', views.StaffDashboardView.as_view(), name='staff_dashboard'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]