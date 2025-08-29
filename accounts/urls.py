from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Registration
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('register/student/', views.StudentRegistrationView.as_view(), name='student_register'),
    path('register/family/', views.FamilyRegistrationView.as_view(), name='family_register'),
    path('register/staff/', views.StaffRegistrationView.as_view(), name='staff_register'),
    path('register/admin/', views.AdministratorRegistrationView.as_view(), name='admin_register'),
    
    # User Profile
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('preferences/', views.UserPreferencesView.as_view(), name='user_preferences'),
    path('dashboard/', views.user_dashboard_data, name='user_dashboard'),
    
    # Students
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    
    # Family
    path('family/', views.FamilyDetailView.as_view(), name='family_detail'),
    path('family/<int:pk>/', views.FamilyDetailView.as_view(), name='family_detail_by_id'),
    
    # Staff
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'),
    
    # Password Management
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<str:uid>/<str:token>/', 
         views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Assignments
    path('assign/student-to-family/', views.assign_student_to_family, name='assign_student_to_family'),
    path('assign/student-to-staff/', views.assign_student_to_staff, name='assign_student_to_staff'),
]