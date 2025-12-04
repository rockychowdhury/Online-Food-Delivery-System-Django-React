from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RestaurantViewSet, BranchViewSet, MenuViewSet, 
    MenuItemViewSet, CuisineViewSet, CategoryViewSet
)

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'cuisines', CuisineViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
