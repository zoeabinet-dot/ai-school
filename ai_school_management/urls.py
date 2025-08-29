"""
URL configuration for ai_school_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponse
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/students/', include('students.urls')),
    path('api/v1/families/', include('families.urls')),
    path('api/v1/staff/', include('staff.urls')),
    path('api/v1/ai-teacher/', include('ai_teacher.urls')),
    path('api/v1/analytics/', include('analytics.urls')),
    path('api/v1/lessons/', include('lessons.urls')),
    path('api/v1/monitoring/', include('monitoring.urls')),
    
    # Root redirect
    path('', RedirectView.as_view(url='/admin/', permanent=False), name='home'),
    
    # Health check
    path('health/', lambda request: HttpResponse('OK'), name='health_check'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Create static directory if it doesn't exist
    static_dir = os.path.join(settings.BASE_DIR, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
