from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Restaurant, Branch, Menu, MenuItem, Cuisine, Category
from .serializers import (
    RestaurantSerializer, BranchSerializer, MenuSerializer, 
    MenuItemSerializer, CuisineSerializer, CategorySerializer,
    RestaurantApprovalSerializer
)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'branches__address__city__name', 'branches__address__street_address']
    filterset_fields = ['is_active', 'is_approved']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        # Public users only see approved and active restaurants
        if self.request.user.is_staff:
            return Restaurant.objects.all()
        return Restaurant.objects.filter(is_approved=True, is_active=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        restaurant = self.get_object()
        serializer = RestaurantApprovalSerializer(restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['name', 'restaurant__name', 'address__city__name']
    filterset_fields = ['branch_type', 'restaurant']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Branch.objects.all()
        # Public sees all branches of approved restaurants
        # TODO: Filter based on branch manager if needed for specific views
        return Branch.objects.filter(restaurant__is_approved=True, restaurant__is_active=True)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['name', 'description', 'category__name']
    filterset_fields = ['category', 'cuisine', 'is_vegetarian', 'is_vegan', 'is_gluten_free', 'is_available']
    ordering_fields = ['price', 'name']

class CuisineViewSet(viewsets.ModelViewSet):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
