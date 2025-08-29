from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )
    password_confirm = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm']
        extra_kwargs = {
            'email': {'allow_blank': False},
            'password':{'write_only':True},
        }
    
    def validate(self, data):
        validated_data = super().validate(data)

        password = validated_data.get('password')
        password_confirm = validated_data.pop('password_confirm', None)

        if password != password_confirm:
            raise serializers.ValidationError({"password_confirm": "Password fields must match."})
        
        try:
            validate_password(password, self.instance)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        
        return validated_data
    
    def validate_email(self, value):
        normalized_email = value.lower().strip() 
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return normalized_email
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone','photoURL', 'bio', 'date_of_birth']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone': {'required': False},
            'photoURL': {'required': False},
            'bio': {'required': False},
        }