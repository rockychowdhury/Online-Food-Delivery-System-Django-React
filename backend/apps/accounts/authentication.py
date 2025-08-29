import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

class JWTCookieAuthentication(BaseAuthentication):
    """Custom JWT authentication using cookies"""
    
    def authenticate(self, request):
        """
        Extract JWT from cookie and authenticate user
        """
        # Get access token from cookie
        access_token = request.COOKIES.get('access_token')
        
        if not access_token:
            return None
            
        try:
            # Decode and validate token
            payload = jwt.decode(
                access_token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            User = get_user_model()
            user = User.objects.get(id=payload['user_id'])
            
            if not user.is_active:
                raise AuthenticationFailed('User account is disabled.')
                
            return (user, access_token)
            
        except jwt.ExpiredSignatureError:
            # Try to refresh token automatically
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                return self._refresh_token(request, refresh_token)
            raise AuthenticationFailed('Access token has expired.')
            
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid access token.')
            
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')
            
        except Exception as e:
            raise AuthenticationFailed('Authentication failed.')

    def _refresh_token(self, request, refresh_token):
        """Attempt to refresh expired access token"""
        try:
            # Validate refresh token
            refresh_payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            
            User = get_user_model()
            user = User.objects.get(id=refresh_payload['user_id'])
            
            if not user.is_active:
                raise AuthenticationFailed('User account is disabled.')
            
            # Generate new access token
            new_access_token = self._generate_access_token(user)
            
            # Set new access token in response (will be handled by middleware)
            request._new_access_token = new_access_token
            
            return (user, new_access_token)
            
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise AuthenticationFailed('Refresh token is invalid or expired.')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')

    def _generate_access_token(self, user):
        """Generate new access token"""
        payload = {
            'user_id': str(user.id),
            'username': user.username,
            'exp': datetime.now() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFETIME),
            'iat': datetime.now(),
        }
        
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


class AuthenticationService:
    """Service class for authentication operations"""
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user with email/password"""
        user = authenticate(email=email, password=password)
        if not user:
            return None, "Invalid credentials"
            
        if not user.is_active:
            return None, "Account is disabled"
            
        return user, None

    @staticmethod
    def generate_token_pair(user):
        """Generate access and refresh token pair"""
        access_payload = {
            'user_id': str(user.id),
            'email': user.email,
            'exp': datetime.now() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFETIME),
            'iat': datetime.now(),
            'type': 'access'
        }
        
        refresh_payload = {
            'user_id': str(user.id),
            'exp': datetime.now() + timedelta(days=settings.JWT_REFRESH_TOKEN_LIFETIME),
            'iat': datetime.now(),
            'type': 'refresh'
        }
        
        access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
        
        return access_token, refresh_token

    @staticmethod
    def set_auth_cookies(response, access_token, refresh_token):
        """Set authentication cookies in response"""
        # Access token cookie (shorter expiry, httpOnly)
        response.set_cookie(
            'access_token',
            access_token,
            max_age=settings.JWT_ACCESS_TOKEN_LIFETIME * 60,  # Convert to seconds
            httponly=True,
            secure=settings.SECURE_COOKIES,
            samesite='Lax'
        )
        
        # Refresh token cookie (longer expiry, httpOnly)
        response.set_cookie(
            'refresh_token',
            refresh_token,
            max_age=settings.JWT_REFRESH_TOKEN_LIFETIME * 24 * 60 * 60,  # Convert to seconds
            httponly=True,
            secure=settings.SECURE_COOKIES,
            samesite='Lax'
        )
        
        return response

    @staticmethod
    def clear_auth_cookies(response):
        """Clear authentication cookies"""
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

    @staticmethod
    def validate_token(token, token_type='access'):
        """Validate JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            if payload.get('type') != token_type:
                return None, "Invalid token type"
                
            User = get_user_model()
            user = User.objects.get(id=payload['user_id'])
            
            if not user.is_active:
                return None, "User account is disabled"
                
            return user, None
            
        except jwt.ExpiredSignatureError:
            return None, "Token has expired"
        except jwt.InvalidTokenError:
            return None, "Invalid token"
        except User.DoesNotExist:
            return None, "User not found"
