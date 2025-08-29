from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    """Home page view"""
    template_name = 'frontend/index.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('frontend:dashboard')
        return super().get(request, *args, **kwargs)


class LoginView(TemplateView):
    """Login page view"""
    template_name = 'frontend/login.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('frontend:dashboard')
        return super().get(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view - redirects to role-specific dashboard"""
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        if user.role == 'student':
            return redirect('frontend:student_dashboard')
        elif user.role == 'family':
            return redirect('frontend:family_dashboard')
        elif user.role == 'staff':
            return redirect('frontend:staff_dashboard')
        elif user.role == 'admin':
            return redirect('frontend:admin_dashboard')
        else:
            return redirect('frontend:index')


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    """Student dashboard view"""
    template_name = 'frontend/student_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'student':
            return redirect('frontend:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.request.user,
            'student_profile': getattr(self.request.user, 'student_profile', None),
        })
        return context


class FamilyDashboardView(LoginRequiredMixin, TemplateView):
    """Family dashboard view"""
    template_name = 'frontend/family_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'family':
            return redirect('frontend:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.request.user,
            'family_profile': getattr(self.request.user, 'family_profile', None),
        })
        return context


class StaffDashboardView(LoginRequiredMixin, TemplateView):
    """Staff dashboard view"""
    template_name = 'frontend/staff_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'staff':
            return redirect('frontend:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.request.user,
            'staff_profile': getattr(self.request.user, 'staff_profile', None),
        })
        return context


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    """Admin dashboard view"""
    template_name = 'frontend/admin_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return redirect('frontend:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.request.user,
            'admin_profile': getattr(self.request.user, 'admin_profile', None),
        })
        return context