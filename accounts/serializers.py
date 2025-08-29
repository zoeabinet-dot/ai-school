from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Student, Family, Staff, Administrator, UserPreferences


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with additional user info"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['role'] = user.role
        token['full_name'] = user.get_full_name()
        token['user_id'] = user.id
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add extra responses
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
            'full_name': self.user.get_full_name(),
            'is_verified': self.user.is_verified,
        }
        
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 
            'first_name', 'last_name', 'role', 'phone_number',
            'date_of_birth', 'address', 'emergency_contact', 'emergency_phone'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'phone_number', 'profile_picture', 'date_of_birth',
            'address', 'emergency_contact', 'emergency_phone', 'is_verified',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentSerializer(serializers.ModelSerializer):
    """Student profile serializer"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'student_id', 'grade_level', 'enrollment_date',
            'learning_preferences', 'special_needs', 'medical_conditions',
            'learning_pace', 'preferred_learning_style', 'attention_span_minutes',
            'is_active'
        ]


class StudentCreateSerializer(serializers.ModelSerializer):
    """Student creation serializer"""
    
    user = UserRegistrationSerializer()
    
    class Meta:
        model = Student
        fields = [
            'user', 'student_id', 'grade_level', 'enrollment_date',
            'learning_preferences', 'special_needs', 'medical_conditions',
            'learning_pace', 'preferred_learning_style', 'attention_span_minutes'
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'student'
        user = UserRegistrationSerializer().create(user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student


class FamilySerializer(serializers.ModelSerializer):
    """Family profile serializer"""
    
    user = UserSerializer(read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Family
        fields = [
            'id', 'user', 'relationship', 'students', 'occupation',
            'workplace', 'preferred_communication', 'notification_preferences'
        ]


class FamilyCreateSerializer(serializers.ModelSerializer):
    """Family creation serializer"""
    
    user = UserRegistrationSerializer()
    
    class Meta:
        model = Family
        fields = [
            'user', 'relationship', 'occupation', 'workplace',
            'preferred_communication', 'notification_preferences'
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'family'
        user = UserRegistrationSerializer().create(user_data)
        family = Family.objects.create(user=user, **validated_data)
        return family


class StaffSerializer(serializers.ModelSerializer):
    """Staff profile serializer"""
    
    user = UserSerializer(read_only=True)
    assigned_students = StudentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Staff
        fields = [
            'id', 'user', 'employee_id', 'position', 'department',
            'hire_date', 'qualifications', 'specializations',
            'assigned_students', 'is_active'
        ]


class StaffCreateSerializer(serializers.ModelSerializer):
    """Staff creation serializer"""
    
    user = UserRegistrationSerializer()
    
    class Meta:
        model = Staff
        fields = [
            'user', 'employee_id', 'position', 'department',
            'hire_date', 'qualifications', 'specializations'
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'staff'
        user = UserRegistrationSerializer().create(user_data)
        staff = Staff.objects.create(user=user, **validated_data)
        return staff


class AdministratorSerializer(serializers.ModelSerializer):
    """Administrator profile serializer"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Administrator
        fields = [
            'id', 'user', 'access_level', 'permissions', 'managed_departments'
        ]


class AdministratorCreateSerializer(serializers.ModelSerializer):
    """Administrator creation serializer"""
    
    user = UserRegistrationSerializer()
    
    class Meta:
        model = Administrator
        fields = [
            'user', 'access_level', 'permissions', 'managed_departments'
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'admin'
        user = UserRegistrationSerializer().create(user_data)
        admin = Administrator.objects.create(user=user, **validated_data)
        return admin


class UserPreferencesSerializer(serializers.ModelSerializer):
    """User preferences serializer"""
    
    class Meta:
        model = UserPreferences
        fields = [
            'theme', 'language', 'timezone', 'notification_settings',
            'dashboard_layout', 'accessibility_settings'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """Password change serializer"""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value


class PasswordResetSerializer(serializers.Serializer):
    """Password reset request serializer"""
    
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Password reset confirmation serializer"""
    
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs