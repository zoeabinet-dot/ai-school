from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import json
import uuid

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, UserProfile, UserSession, Permission, RolePermission
from .serializers import (
    UserSerializer, UserProfileSerializer, UserRegistrationSerializer,
    PasswordChangeSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
)


class UserRegistrationView(APIView):
    """
    User registration endpoint
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    
                    # Create user profile
                    UserProfile.objects.create(user=user)
                    
                    # Send email verification
                    self.send_verification_email(user)
                    
                    # Generate tokens
                    refresh = RefreshToken.for_user(user)
                    
                    return Response({
                        'message': 'User registered successfully. Please check your email for verification.',
                        'user': UserSerializer(user).data,
                        'tokens': {
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                        }
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                return Response({
                    'error': 'Registration failed. Please try again.',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_verification_email(self, user):
        """Send email verification email"""
        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"
            
            subject = 'Verify Your Email - AI School Management System'
            message = render_to_string('accounts/email_verification.html', {
                'user': user,
                'verification_url': verification_url,
            })
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message
            )
            
            # Update user with verification token
            user.email_verification_token = token
            user.save()
            
        except Exception as e:
            print(f"Failed to send verification email: {e}")


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain view with additional user data
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get user data
            user = User.objects.get(username=request.data['username'])
            user_data = UserSerializer(user).data
            
            # Track session
            self.track_user_session(user, request)
            
            # Add user data to response
            response.data['user'] = user_data
            
        return response
    
    def track_user_session(self, user, request):
        """Track user login session"""
        try:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            
            UserSession.objects.create(
                user=user,
                session_key=session_key,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                is_active=True
            )
        except Exception as e:
            print(f"Failed to track user session: {e}")
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserProfileView(APIView):
    """
    Get and update user profile
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        """Update user profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class UserProfileUpdateView(APIView):
    """
    Update user profile and basic information
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        """Update user and profile information"""
        try:
            user = request.user
            profile = UserProfile.objects.get(user=user)
            
            # Update user fields
            user_serializer = UserSerializer(user, data=request.data.get('user', {}), partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            
            # Update profile fields
            profile_serializer = UserProfileSerializer(profile, data=request.data.get('profile', {}), partial=True)
            if profile_serializer.is_valid():
                profile_serializer.save()
            
            return Response({
                'user': UserSerializer(user).data,
                'profile': UserProfileSerializer(profile).data
            })
            
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    """
    Change user password
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({'message': 'Password changed successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """
    Request password reset
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                self.send_password_reset_email(user)
                
                return Response({
                    'message': 'Password reset email sent successfully'
                })
                
            except User.DoesNotExist:
                return Response({
                    'message': 'If an account with this email exists, a password reset email has been sent'
                })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_password_reset_email(self, user):
        """Send password reset email"""
        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            
            subject = 'Reset Your Password - AI School Management System'
            message = render_to_string('accounts/password_reset.html', {
                'user': user,
                'reset_url': reset_url,
            })
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message
            )
            
        except Exception as e:
            print(f"Failed to send password reset email: {e}")


class PasswordResetConfirmView(APIView):
    """
    Confirm password reset with token
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
                user = User.objects.get(pk=uid)
                
                # Check token validity
                if default_token_generator.check_token(user, serializer.validated_data['token']):
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    
                    return Response({'message': 'Password reset successfully'})
                else:
                    return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
                    
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({'error': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    """
    Request email verification
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        if user.email_verified:
            return Response({'message': 'Email already verified'})
        
        # Send verification email
        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"
            
            subject = 'Verify Your Email - AI School Management System'
            message = render_to_string('accounts/email_verification.html', {
                'user': user,
                'verification_url': verification_url,
            })
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message
            )
            
            # Update verification token
            user.email_verification_token = token
            user.save()
            
            return Response({'message': 'Verification email sent successfully'})
            
        except Exception as e:
            return Response({'error': 'Failed to send verification email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailVerificationConfirmView(APIView):
    """
    Confirm email verification with token
    """
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            # Check token validity
            if default_token_generator.check_token(user, token):
                user.email_verified = True
                user.email_verification_token = ''
                user.save()
                
                return Response({'message': 'Email verified successfully'})
            else:
                return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)
                
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    """
    List all users (admin only)
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    """
    Get user details (admin only)
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserUpdateView(APIView):
    """
    Update user (admin only)
    """
    permission_classes = [IsAdminUser]
    
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    """
    Delete user (admin only)
    """
    permission_classes = [IsAdminUser]
    
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({'message': 'User deleted successfully'})


class StudentListView(APIView):
    """
    List all students
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        students = User.objects.filter(role=User.UserRole.STUDENT)
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)


class FamilyListView(APIView):
    """
    List all family members
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        families = User.objects.filter(role=User.UserRole.FAMILY)
        serializer = UserSerializer(families, many=True)
        return Response(serializer.data)


class StaffListView(APIView):
    """
    List all staff members
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        staff = User.objects.filter(role=User.UserRole.STAFF)
        serializer = UserSerializer(staff, many=True)
        return Response(serializer.data)


class UserSessionListView(APIView):
    """
    List user sessions
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_admin:
            sessions = UserSession.objects.all()
        else:
            sessions = UserSession.objects.filter(user=request.user)
        
        # Convert to list for serialization
        session_data = []
        for session in sessions:
            session_data.append({
                'id': session.id,
                'user': session.user.username,
                'login_time': session.login_time,
                'logout_time': session.logout_time,
                'ip_address': session.ip_address,
                'is_active': session.is_active
            })
        
        return Response(session_data)


class UserSessionDetailView(APIView):
    """
    Get session details
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        session = get_object_or_404(UserSession, pk=pk)
        
        # Check permissions
        if not request.user.is_admin and session.user != request.user:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        session_data = {
            'id': session.id,
            'user': session.user.username,
            'session_key': session.session_key,
            'login_time': session.login_time,
            'logout_time': session.logout_time,
            'ip_address': session.ip_address,
            'user_agent': session.user_agent,
            'is_active': session.is_active
        }
        
        return Response(session_data)


class PermissionListView(APIView):
    """
    List all permissions
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        permissions = Permission.objects.all()
        permission_data = []
        
        for perm in permissions:
            permission_data.append({
                'id': perm.id,
                'name': perm.name,
                'codename': perm.codename,
                'description': perm.description
            })
        
        return Response(permission_data)


class RolePermissionListView(APIView):
    """
    List role permissions
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        role_permissions = RolePermission.objects.all()
        role_perm_data = []
        
        for rp in role_permissions:
            role_perm_data.append({
                'id': rp.id,
                'role': rp.role,
                'permission': rp.permission.name,
                'permission_codename': rp.permission.codename
            })
        
        return Response(role_perm_data)


class LogoutView(APIView):
    """
    Logout user and invalidate session
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Mark session as inactive
            UserSession.objects.filter(
                user=request.user,
                session_key=request.session.session_key,
                is_active=True
            ).update(
                is_active=False,
                logout_time=timezone.now()
            )
            
            # Logout user
            logout(request)
            
            return Response({'message': 'Logged out successfully'})
            
        except Exception as e:
            return Response({'error': 'Logout failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
