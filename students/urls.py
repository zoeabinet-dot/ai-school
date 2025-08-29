from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Placeholder URLs - to be implemented
    path('', views.student_list, name='student_list'),
]

# Placeholder view to avoid import errors
def student_list(request):
    from django.http import JsonResponse
    return JsonResponse({'message': 'Students endpoint - to be implemented'})