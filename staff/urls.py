from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    # Staff management
    path('', views.StaffListView.as_view(), name='staff_list'),
    path('create/', views.StaffCreateView.as_view(), name='staff_create'),
    path('<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'),
    
    # Staff dashboard
    path('<int:staff_id>/dashboard/', views.StaffDashboardView.as_view(), name='staff_dashboard'),
    
    # Legacy endpoint for backward compatibility
    path('legacy/', views.staff_list, name='staff_list_legacy'),
]
