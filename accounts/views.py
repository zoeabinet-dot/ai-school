from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import User, Student, Family, Staff, Administrator, UserPreferences
from .serializers import (
    CustomTokenObtainPairSerializer, UserRegistrationSerializer, UserSerializer,
    StudentSerializer, StudentCreateSerializer, FamilySerializer, FamilyCreateSerializer,
    StaffSerializer, StaffCreateSerializer, AdministratorSerializer, AdministratorCreateSerializer,
    UserPreferencesSerializer, PasswordChangeSerializer, PasswordResetSerializer,
    PasswordResetConfirmSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view with additional user info"""
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile view"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class StudentRegistrationView(generics.CreateAPIView):
    """Student registration endpoint"""
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer
    permission_classes = [permissions.AllowAny]  # Or restrict to admin/staff
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        
        return Response({
            'student': StudentSerializer(student).data,
            'message': 'Student registered successfully'
        }, status=status.HTTP_201_CREATED)


class StudentListView(generics.ListAPIView):
    """List all students"""
    queryset = Student.objects.filter(is_active=True)
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Student.objects.filter(is_active=True)
        elif user.role == 'staff':
            return user.staff_profile.assigned_students.filter(is_active=True)
        elif user.role == 'family':
            return user.family_profile.students.filter(is_active=True)
        elif user.role == 'student':
            return Student.objects.filter(user=user)
        return Student.objects.none()


class StudentDetailView(generics.RetrieveUpdateAPIView):
    """Student detail view"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Student.objects.all()
        elif user.role == 'staff':
            return user.staff_profile.assigned_students.all()
        elif user.role == 'family':
            return user.family_profile.students.all()
        elif user.role == 'student':
            return Student.objects.filter(user=user)
        return Student.objects.none()


class FamilyRegistrationView(generics.CreateAPIView):
    """Family registration endpoint"""
    queryset = Family.objects.all()
    serializer_class = FamilyCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        family = serializer.save()
        
        return Response({
            'family': FamilySerializer(family).data,
            'message': 'Family member registered successfully'
        }, status=status.HTTP_201_CREATED)


class FamilyDetailView(generics.RetrieveUpdateAPIView):
    """Family detail view"""
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if self.request.user.role == 'family':
            return self.request.user.family_profile
        return super().get_object()


class StaffRegistrationView(generics.CreateAPIView):
    """Staff registration endpoint"""
    queryset = Staff.objects.all()
    serializer_class = StaffCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only admin can create staff
    
    def create(self, request, *args, **kwargs):
        # Check if user is admin
        if request.user.role != 'admin':
            return Response(
                {'error': 'Only administrators can register staff members'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff = serializer.save()
        
        return Response({
            'staff': StaffSerializer(staff).data,
            'message': 'Staff member registered successfully'
        }, status=status.HTTP_201_CREATED)


class StaffListView(generics.ListAPIView):
    """List all staff members"""
    queryset = Staff.objects.filter(is_active=True)
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role in ['admin', 'staff']:
            return Staff.objects.filter(is_active=True)
        return Staff.objects.none()


class StaffDetailView(generics.RetrieveUpdateAPIView):
    """Staff detail view"""
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if self.request.user.role == 'staff':
            return self.request.user.staff_profile
        return super().get_object()


class AdministratorRegistrationView(generics.CreateAPIView):
    """Administrator registration endpoint"""
    queryset = Administrator.objects.all()
    serializer_class = AdministratorCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Check if user is super admin
        if not (request.user.role == 'admin' and 
                hasattr(request.user, 'admin_profile') and 
                request.user.admin_profile.access_level == 'super'):
            return Response(
                {'error': 'Only super administrators can register new administrators'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin = serializer.save()
        
        return Response({
            'administrator': AdministratorSerializer(admin).data,
            'message': 'Administrator registered successfully'
        }, status=status.HTTP_201_CREATED)


class UserPreferencesView(generics.RetrieveUpdateAPIView):
    """User preferences view"""
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        preferences, created = UserPreferences.objects.get_or_create(
            user=self.request.user
        )
        return preferences


class PasswordChangeView(APIView):
    """Password change view"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """Password reset request view"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Generate reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Send email (implement email sending logic)
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            
            try:
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                return Response({
                    'message': 'Password reset email sent successfully'
                }, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({
                    'error': 'Failed to send email'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """Password reset confirmation view"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, uid, token):
        try:
            # Decode user ID
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
            
            # Validate token
            if not default_token_generator.check_token(user, token):
                return Response({
                    'error': 'Invalid or expired token'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = PasswordResetConfirmSerializer(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                
                return Response({
                    'message': 'Password reset successfully'
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'error': 'Invalid user'
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Logout view"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Logged out successfully'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard_data(request):
    """Get user-specific dashboard data"""
    user = request.user
    data = {
        'user': UserSerializer(user).data,
        'role_data': {}
    }
    
    if user.role == 'student':
        if hasattr(user, 'student_profile'):
            data['role_data'] = StudentSerializer(user.student_profile).data
    elif user.role == 'family':
        if hasattr(user, 'family_profile'):
            data['role_data'] = FamilySerializer(user.family_profile).data
    elif user.role == 'staff':
        if hasattr(user, 'staff_profile'):
            data['role_data'] = StaffSerializer(user.staff_profile).data
    elif user.role == 'admin':
        if hasattr(user, 'admin_profile'):
            data['role_data'] = AdministratorSerializer(user.admin_profile).data
    
    return Response(data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def assign_student_to_family(request):
    """Assign a student to a family member"""
    if request.user.role not in ['admin', 'staff']:
        return Response(
            {'error': 'Permission denied'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    student_id = request.data.get('student_id')
    family_id = request.data.get('family_id')
    
    try:
        student = Student.objects.get(id=student_id)
        family = Family.objects.get(id=family_id)
        
        family.students.add(student)
        
        return Response({
            'message': f'Student {student.user.get_full_name()} assigned to {family.user.get_full_name()}'
        }, status=status.HTTP_200_OK)
    
    except (Student.DoesNotExist, Family.DoesNotExist) as e:
        return Response(
            {'error': 'Student or family member not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def assign_student_to_staff(request):
    """Assign a student to a staff member"""
    if request.user.role not in ['admin']:
        return Response(
            {'error': 'Only administrators can assign students to staff'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    student_id = request.data.get('student_id')
    staff_id = request.data.get('staff_id')
    
    try:
        student = Student.objects.get(id=student_id)
        staff = Staff.objects.get(id=staff_id)
        
        staff.assigned_students.add(student)
        
        return Response({
            'message': f'Student {student.user.get_full_name()} assigned to {staff.user.get_full_name()}'
        }, status=status.HTTP_200_OK)
    
    except (Student.DoesNotExist, Staff.DoesNotExist) as e:
        return Response(
            {'error': 'Student or staff member not found'},
            status=status.HTTP_404_NOT_FOUND
        )