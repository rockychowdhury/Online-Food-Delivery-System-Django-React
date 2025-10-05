import jwt
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.common.utils.responses import ResponseMessages

logger = logging.getLogger(__name__)
User = get_user_model()


class JWTCookieAuthentication(BaseAuthentication):
    """Custom JWT authentication using cookies"""
    
    def authenticate(self, request):
        """ Extract JWT from cookie and authenticate user """
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
            user = User.objects.get(id=payload['user_id'])
            
            if not user.is_active:
                logger.warning(f"Disabled user attempted login: {user.email}")
                raise AuthenticationFailed(ResponseMessages.ACCOUNT_DISABLED)
                
            return (user, access_token)
            
        except jwt.ExpiredSignatureError:
            # Try to refresh token automatically
            logger.info("Access token expired, attempting refresh")
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                return self._refresh_token(request, refresh_token)
            raise AuthenticationFailed(ResponseMessages.TOKEN_EXPIRED)
            
        except jwt.InvalidTokenError:
            logger.warning("Invalid access token provided")
            raise AuthenticationFailed(ResponseMessages.TOKEN_INVALID)
            
        except User.DoesNotExist:
            logger.error("User not found for valid token")
            raise AuthenticationFailed(ResponseMessages.USER_NOT_FOUND)
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise AuthenticationFailed(ResponseMessages.AUTHENTICATION_FAILED)

    def _refresh_token(self, request, refresh_token):
        """Attempt to refresh expired access token"""
        try:
            # Validate refresh token
            refresh_payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            
            user = User.objects.get(id=refresh_payload['user_id'])
            
            if not user.is_active:
                raise AuthenticationFailed(ResponseMessages.ACCOUNT_DISABLED)
            
            # Generate new access token
            new_access_token = self._generate_access_token(user)
            
            # Set new access token in response (will be handled by middleware)
            request._new_access_token = new_access_token
            logger.info(f"Token refreshed for user: {user.email}")

            return (user, new_access_token)
            
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            logger.warning("Invalid or expired refresh token")
            raise AuthenticationFailed(ResponseMessages.TOKEN_INVALID)
        except User.DoesNotExist:
            logger.error("User not found for refresh token")
            raise AuthenticationFailed(ResponseMessages.USER_NOT_FOUND)
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            raise AuthenticationFailed(ResponseMessages.TOKEN_REFRESH_FAILED)

    def _generate_access_token(self, user):
        """Generate new access token"""
        payload = {
            'user_id': str(user.id),
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_LIFETIME),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


class AuthenticationService:
    """Service class for authentication operations"""
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user with email/password"""
        user = authenticate(email=email, password=password)
        if not user:
            return None, ResponseMessages.INVALID_CREDENTIALS
            
        if not user.is_active:
            return None, ResponseMessages.ACCOUNT_DISABLED
            
        return user, None

    @staticmethod
    def generate_token_pair(user):
        """Generate access and refresh token pair"""
        access_payload = {
            'user_id': str(user.id),
            'email': user.email,
            'role': user.get_active_role().role.name if user.get_active_role() else None,
            'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFETIME),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        refresh_payload = {
            'user_id': str(user.id),
            'exp': datetime.now() + timedelta(days=settings.JWT_REFRESH_TOKEN_LIFETIME),
            'iat': datetime.now(),
            'type': 'refresh',
        }
        
        access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
        logger.info(f"Token pair generated for user: {user.email}")
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
                return None, ResponseMessages.TOKEN_INVALID
            
            user = User.objects.get(id=payload['user_id'])
            
            if not user.is_active:
                return None, ResponseMessages.ACCOUNT_DISABLED
                
            return user, None
            
        except jwt.ExpiredSignatureError:
            return None, ResponseMessages.TOKEN_EXPIRED
        except jwt.InvalidTokenError:
            return None, ResponseMessages.TOKEN_INVALID
        except User.DoesNotExist:
            return None, ResponseMessages.USER_NOT_FOUND
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            return None, ResponseMessages.TOKEN_VALIDATION_FAILED
