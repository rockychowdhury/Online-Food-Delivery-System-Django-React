from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from apps.common.utils.validators import validate_password_strength
from apps.common.utils.responses import ResponseMessages
from django.core import exceptions

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
        }
    
    def validate_email(self, value):
        """Validate email uniqueness"""
        email = value.lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(ResponseMessages.USER_ALREADY_EXISTS)
        return email
    
    def validate_password(self, value):
        """Validate password strength"""
        validate_password(value)  # Django's built-in validation
        validate_password_strength(value)  # custom validation
        return value
    
    def create(self, validated_data):
        """Create user with validated data"""
        return User.objects.create_user(**validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'photo_url', 'bio', 'date_of_birth']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone': {'required': False},
            'photo_url': {'required': False},
            'bio': {'required': False, 'max_length': 500},
            'date_of_birth': {'required': False},
        }

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for displaying user profile"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    active_role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'photo_url', 'bio', 'date_of_birth',
            'is_verified', 'is_email_verified', 'is_phone_verified',
            'active_role', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email', 'is_verified', 'created_at', 'updated_at']
    
    def get_active_role(self, obj):
        """Get user's active role information"""
        active_role = obj.get_active_role()
        if active_role:
            return {
                'name': active_role.role.name,
                'role_type': active_role.role.role_type,
                'assigned_at': active_role.assigned_at,
                'expires_at': active_role.expires_at,
            }
        return None


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    
    def validate_new_password(self, value):
        """Validate new password"""
        validate_password(value)
        validate_password_strength(value)
        return value