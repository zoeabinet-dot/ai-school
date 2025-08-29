from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

app_name = 'accounts'

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User registration and management
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='user_profile_update'),
    
    # Password management
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Email verification
    path('verify-email/', views.EmailVerificationView.as_view(), name='email_verification'),
    path('verify-email/confirm/<str:token>/', views.EmailVerificationConfirmView.as_view(), name='email_verification_confirm'),
    
    # User management (admin only)
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    
    # Role-based endpoints
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('families/', views.FamilyListView.as_view(), name='family_list'),
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    
    # Session management
    path('sessions/', views.UserSessionListView.as_view(), name='session_list'),
    path('sessions/<int:pk>/', views.UserSessionDetailView.as_view(), name='session_detail'),
    
    # Permission management
    path('permissions/', views.PermissionListView.as_view(), name='permission_list'),
    path('role-permissions/', views.RolePermissionListView.as_view(), name='role_permission_list'),
    
    # Logout
    path('logout/', views.LogoutView.as_view(), name='logout'),
]