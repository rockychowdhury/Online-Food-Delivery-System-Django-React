from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .authentication import AuthenticationService
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .serializers import UserRegistrationSerializer, UserUpdateSerializer

class LoginView(APIView):
    """User login with JWT cookie authentication"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'error': 'Credentials not provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate user
        user, error = AuthenticationService.authenticate_user(email, password)
        
        if error:
            return Response({
                'error': error
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate tokens
        access_token, refresh_token = AuthenticationService.generate_token_pair(user)
        
        response_data = {
            'message': 'Login successful',
            'user': {
                'id': str(user.id),
                'email': user.email,
            }
        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        
        # Set authentication cookies
        response = AuthenticationService.set_auth_cookies(response, access_token, refresh_token)
        
        return response


class LogoutView(APIView):
    """User logout - clear cookies"""
    
    def post(self, request):
        response_data = {'message': 'Logout successful'}
        response = Response(response_data, status=status.HTTP_200_OK)
        
        # Clear authentication cookies
        response = AuthenticationService.clear_auth_cookies(response)
        
        return response


class RefreshTokenView(APIView):
    """Refresh access token using refresh token"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token not found'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Validate refresh token
        user, error = AuthenticationService.validate_token(refresh_token, 'refresh')
        
        if error:
            return Response({
                'error': error
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate new token pair
        access_token, new_refresh_token = AuthenticationService.generate_token_pair(user)
        
        response_data = {
            'message': 'Tokens refreshed successfully'
        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        
        # Set new authentication cookies
        response = AuthenticationService.set_auth_cookies(response, access_token, new_refresh_token)
        
        return response


class ProfileView(APIView):
    permission_classes =[IsAuthenticated]
    
    def get(self, request):
        user = request.user
        active_role = user.get_active_role()
        
        user_data = {
            'id': str(user.id),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'role': {
                'name': active_role.role.name,
                'display_name': active_role.role.display_name,
                'assigned_at': active_role.assigned_at,
                'expires_at': active_role.expires_at,
            } if active_role else None,
        }
        
        return Response(user_data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        user= request.user
        serializer = UserUpdateSerializer(user, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = serializer.save()
        except Exception as e:
            return Response(
                {"detail": "An error occurred during user creation. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response_data = {
            "message": "User created successfully.",
            "user": {
                "id": user.id,
                "email": user.email
            },
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response(
                {"error": "The old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            validate_password(new_password,user)
        except ValidationError as e:
            return Response(
                {"error": e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password updated successfully."},
            status=status.HTTP_200_OK
        )


