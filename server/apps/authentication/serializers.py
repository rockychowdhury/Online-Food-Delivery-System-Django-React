from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed


User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            return super().validate(attrs)

        if user and not user.is_active:
            raise AuthenticationFailed(
                detail={'detail': 'Your account has been deactivated.', 'code': 'account_deactivated'}
            )

        return super().validate(attrs)
    
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','first_name','last_name']
        extra_kwargs = {
            "password":{"write_only":True},
            }
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number','photoURL','bio']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'photoURL': {'required': False},
            'bio': {'required': False},
        }