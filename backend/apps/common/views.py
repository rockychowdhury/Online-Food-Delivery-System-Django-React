from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import connection
from apps.common.utils import APIResponse
from time import timezone

class HealthCheckView(APIView):
    """Health check endpoint for monitoring"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Check application health"""
        try:
            # Check database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                
            health_data = {
                'status': 'healthy',
                'database': 'connected',
                'timestamp': timezone.now().isoformat()
            }
            
            return APIResponse.success(
                message="Application is healthy",
                data=health_data
            )
        except Exception as e:
            return APIResponse.error(
                message="Health check failed",
                errors=str(e),
                status_code=503
            )