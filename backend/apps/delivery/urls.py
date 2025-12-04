from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeliveryPartnerViewSet, DeliveryStatusViewSet

router = DefaultRouter()
router.register(r'partners', DeliveryPartnerViewSet)
router.register(r'statuses', DeliveryStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
