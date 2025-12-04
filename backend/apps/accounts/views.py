import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from apps.common.utils import APIResponse, ResponseMessages
from .authentication import AuthenticationService
from .serializers import (
    UserRegistrationSerializer, 
    UserUpdateSerializer, 
    UserProfileSerializer,
    UserProfileSerializer,
    PasswordChangeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer,
    PhoneVerificationSerializer
)

logger = logging.getLogger(__name__)

class LoginView(APIView):
    """User login with JWT cookie authentication"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password')
        
        if not email or not password:
            return APIResponse.error(
                message=ResponseMessages.MISSING_CREDENTIALS,
                error_code="MISSING_CREDENTIALS"
            )
        
        # Authenticate user
        user, error = AuthenticationService.authenticate_user(email, password)
        
        if error:
            return APIResponse.error(
                message=error,
                error_code="AUTHENTICATION_FAILED",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate tokens
        access_token, refresh_token = AuthenticationService.generate_token_pair(user)
        
        user_data = {
            'id': str(user.id),
            'email': user.email,
            'full_name': user.get_full_name(),
            'is_verified': user.is_verified,
        }
        
        response = APIResponse.success(message=ResponseMessages.LOGIN_SUCCESS,data=user_data)
        
        # Set authentication cookies
        response = AuthenticationService.set_auth_cookies(response, access_token, refresh_token)
        
        return response


class LogoutView(APIView):
    """User logout - clear cookies"""
    
    def post(self, request):
        if request.user and hasattr(request.user, 'email'):
            logger.info(f"User logged out: {request.user.email}")

        response = APIResponse.success(message=ResponseMessages.LOGOUT_SUCCESS)
        # Clear authentication cookies
        response = AuthenticationService.clear_auth_cookies(response)
        
        return response


class RefreshTokenView(APIView):
    """Refresh access token using refresh token"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return APIResponse.error(
                message="Refresh token not found",
                error_code="REFRESH_TOKEN_MISSING",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        # Validate refresh token
        user, error = AuthenticationService.validate_token(refresh_token, 'refresh')
        
        if error:
            return APIResponse.error(
                message=error,
                error_code="REFRESH_TOKEN_INVALID",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate new token pair
        access_token, new_refresh_token = AuthenticationService.generate_token_pair(user)
        
        response = APIResponse.success(message=ResponseMessages.TOKEN_REFRESHED)
        
        # Set new authentication cookies
        response = AuthenticationService.set_auth_cookies(response, access_token, new_refresh_token)

        logger.info(f"Tokens refreshed for user: {user.email}")
        return response


class ProfileView(APIView):
    """User profile management"""
    permission_classes =[IsAuthenticated]
    
    def get(self, request):
        """Get user profile"""
        serializer = UserProfileSerializer(request.user)

        return APIResponse.success(
            message=ResponseMessages.PROFILE_RETRIEVED,
            data=serializer.data
        )
    
    def patch(self, request):
        """Update user profile"""
        serializer = UserUpdateSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Profile updated for user: {request.user.email}")
            return APIResponse.success(
                message=ResponseMessages.PROFILE_UPDATED,
                data=serializer.data
            )
        return APIResponse.error(
            message=ResponseMessages.VALIDATION_ERROR,
            errors=serializer.errors,
            error_code="VALIDATION_ERROR"
        )

class UserRegistrationView(APIView):
    """User registration"""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"New user registered: {user.email}")

            # TODO: Send verification email

            response_data = {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.get_full_name(),
            }
            return APIResponse.success(
                message=ResponseMessages.REGISTRATION_SUCCESS,
                data=response_data,
                status_code=status.HTTP_201_CREATED
            )
        
        return APIResponse.error(
            message=ResponseMessages.VALIDATION_ERROR,
            errors=serializer.errors,
            error_code="REGISTRATION_VALIDATION_ERROR"
        )


class PasswordChangeView(APIView):
    """Change user password"""
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = PasswordChangeSerializer(data=request.data)

        if not serializer.is_valid():
            return APIResponse.error(
                message=ResponseMessages.VALIDATION_ERROR,
                errors=serializer.errors,
                error_code="VALIDATION_ERROR"
            )

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return APIResponse.error(
                message=ResponseMessages.OLD_PASSWORD_INCORRECT,
                error_code="OLD_PASSWORD_INCORRECT"
            )
        
        user.set_password(new_password)
        user.save()

        logger.info(f"Password changed for user: {user.email}")

        return APIResponse.success(message=ResponseMessages.PASSWORD_CHANGED)

        return APIResponse.success(message=ResponseMessages.PASSWORD_CHANGED)

#TODO: Implement password reset email verification
class PasswordResetRequestView(APIView):
    """Request password reset email"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(
                message=ResponseMessages.VALIDATION_ERROR,
                errors=serializer.errors
            )

        email = serializer.validated_data['email']
        # In a real app, we would check if user exists and send email
        # For now, we'll just simulate success to avoid enumeration attacks
        logger.info(f"Password reset requested for: {email}")
        
        return APIResponse.success(message="If an account exists with this email, a password reset link has been sent.")

#TODO: Implement password reset confirmation

class PasswordResetConfirmView(APIView):
    """Confirm password reset"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(
                message=ResponseMessages.VALIDATION_ERROR,
                errors=serializer.errors
            )

        # In a real app, we would validate token/uidb64 and reset password
        # For this implementation, we'll mock the success
        
        return APIResponse.success(message="Password has been reset successfully.")

class RequestEmailVerificationView(APIView):
    """Request email verification link"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.is_email_verified:
            return APIResponse.error(
                message="Email is already verified",
                error_code="EMAIL_ALREADY_VERIFIED"
            )
        
        # TODO: Generate token and send email
        logger.info(f"Email verification requested for: {user.email}")
        
        return APIResponse.success(message="Verification email sent successfully")

class VerifyEmailView(APIView):
    """Verify email with token"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(
                message=ResponseMessages.VALIDATION_ERROR,
                errors=serializer.errors
            )
        
        token = serializer.validated_data['token']
        # TODO: Validate token and update user.is_email_verified
        
        return APIResponse.success(message="Email verified successfully")

class RequestPhoneVerificationView(APIView):
    """Request phone verification OTP"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.phone:
            return APIResponse.error(
                message="Phone number not set",
                error_code="PHONE_NOT_SET"
            )
            
        if user.is_phone_verified:
            return APIResponse.error(
                message="Phone is already verified",
                error_code="PHONE_ALREADY_VERIFIED"
            )
        
        # TODO: Generate OTP and send SMS
        logger.info(f"Phone verification requested for: {user.phone}")
        
        return APIResponse.success(message="Verification OTP sent successfully")

class VerifyPhoneView(APIView):
    """Verify phone with OTP"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PhoneVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(
                message=ResponseMessages.VALIDATION_ERROR,
                errors=serializer.errors
            )
        
        otp = serializer.validated_data['otp']
        # TODO: Validate OTP and update user.is_phone_verified
        
        return APIResponse.success(message="Phone verified successfully")
