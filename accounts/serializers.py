from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, UserSession, Permission, RolePermission

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'role_display', 'phone_number', 'date_of_birth',
            'profile_picture', 'address', 'city', 'country', 'bio',
            'is_active', 'email_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'email_verified']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def validate_email(self, value):
        """Ensure email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        """Ensure username is unique"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'grade_level', 'academic_year',
            'relationship_to_student', 'department', 'position', 'hire_date',
            'language_preference', 'notification_preferences',
            'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relationship', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'role', 'phone_number',
            'date_of_birth', 'address', 'city', 'country', 'bio'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True}
        }
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def validate_role(self, value):
        """Validate user role"""
        allowed_roles = [User.UserRole.STUDENT, User.UserRole.FAMILY, User.UserRole.STAFF]
        if value not in allowed_roles:
            raise serializers.ValidationError("Invalid role selected.")
        return value
    
    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset request
    """
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        """Validate email exists"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation
    """
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information
    """
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'date_of_birth',
            'profile_picture', 'address', 'city', 'country', 'bio'
        ]
    
    def validate_email(self, value):
        """Ensure email is unique if changed"""
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile
    """
    class Meta:
        model = UserProfile
        fields = [
            'grade_level', 'academic_year', 'relationship_to_student',
            'department', 'position', 'hire_date', 'language_preference',
            'notification_preferences', 'emergency_contact_name',
            'emergency_contact_phone', 'emergency_contact_relationship'
        ]


class UserSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for UserSession model
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserSession
        fields = [
            'id', 'user', 'session_key', 'ip_address', 'user_agent',
            'login_time', 'logout_time', 'is_active'
        ]
        read_only_fields = ['id', 'user', 'session_key', 'login_time']


class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Permission model
    """
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'description']


class RolePermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for RolePermission model
    """
    permission = PermissionSerializer(read_only=True)
    
    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission']


class UserListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for user lists
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 'role', 'role_display',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for user information
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'role_display', 'phone_number', 'date_of_birth',
            'profile_picture', 'address', 'city', 'country', 'bio',
            'is_active', 'email_verified', 'created_at', 'updated_at',
            'profile'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserSearchSerializer(serializers.Serializer):
    """
    Serializer for user search
    """
    query = serializers.CharField(max_length=100, required=False)
    role = serializers.ChoiceField(choices=User.UserRole.choices, required=False)
    is_active = serializers.BooleanField(required=False)
    created_after = serializers.DateField(required=False)
    created_before = serializers.DateField(required=False)


class UserBulkUpdateSerializer(serializers.Serializer):
    """
    Serializer for bulk user updates
    """
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    updates = serializers.DictField()
    
    def validate_updates(self, value):
        """Validate update fields"""
        allowed_fields = [
            'is_active', 'role', 'first_name', 'last_name',
            'phone_number', 'city', 'country'
        ]
        
        for field in value.keys():
            if field not in allowed_fields:
                raise serializers.ValidationError(f"Field '{field}' is not allowed for bulk updates.")
        
        return value


class UserExportSerializer(serializers.ModelSerializer):
    """
    Serializer for user data export
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    profile_data = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'role_display', 'phone_number', 'date_of_birth',
            'address', 'city', 'country', 'bio', 'is_active', 'email_verified',
            'created_at', 'updated_at', 'profile_data'
        ]
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_profile_data(self, obj):
        """Get profile data for export"""
        try:
            profile = obj.profile
            return {
                'grade_level': profile.grade_level,
                'academic_year': profile.academic_year,
                'relationship_to_student': profile.relationship_to_student,
                'department': profile.department,
                'position': profile.position,
                'hire_date': profile.hire_date,
                'language_preference': profile.language_preference,
                'emergency_contact_name': profile.emergency_contact_name,
                'emergency_contact_phone': profile.emergency_contact_phone,
            }
        except UserProfile.DoesNotExist:
            return {}