from django.urls import path
from . import views

app_name = 'families'

urlpatterns = [
    # Family management
    path('', views.FamilyListView.as_view(), name='family_list'),
    path('create/', views.FamilyCreateView.as_view(), name='family_create'),
    path('<int:pk>/', views.FamilyDetailView.as_view(), name='family_detail'),
    
    # Family members
    path('<int:family_id>/members/', views.FamilyMemberListView.as_view(), name='family_member_list'),
    path('<int:family_id>/members/create/', views.FamilyMemberCreateView.as_view(), name='family_member_create'),
    
    # Family students
    path('<int:family_id>/students/', views.FamilyStudentListView.as_view(), name='family_student_list'),
    path('<int:family_id>/students/create/', views.FamilyStudentCreateView.as_view(), name='family_student_create'),
    
    # Family dashboard
    path('<int:family_id>/dashboard/', views.FamilyDashboardView.as_view(), name='family_dashboard'),
    
    # Family search
    path('search/', views.FamilySearchView.as_view(), name='family_search'),
    
    # Legacy endpoint for backward compatibility
    path('legacy/', views.family_list, name='family_list_legacy'),
]
