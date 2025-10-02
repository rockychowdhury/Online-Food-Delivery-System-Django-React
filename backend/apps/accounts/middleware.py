import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class CookieRefreshMiddleware:
    """Middleware to handle automatic token refresh"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # If a new access token was generated during authentication
        if hasattr(request, '_new_access_token'):
            logger.debug("Setting new access token in cookie")
            response.set_cookie(
                'access_token',
                request._new_access_token,
                max_age=settings.JWT_ACCESS_TOKEN_LIFETIME * 60,
                httponly=True,
                secure=settings.SECURE_COOKIES,
                samesite='Lax'
            )
        
        return response