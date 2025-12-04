from rest_framework.views import APIView
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemCreateSerializer, CartItemUpdateSerializer
from apps.common.utils import APIResponse, ResponseMessages

class CartView(APIView):
    """Get current user's cart"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return APIResponse.success(data=serializer.data)

class AddToCartView(APIView):
    """Add item to cart"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            menu_item = serializer.validated_data['menu_item']
            quantity = serializer.validated_data['quantity']
            
            # Check if item already exists in cart
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart, 
                menu_item=menu_item,
                defaults={'quantity': quantity}
            )
            
            if not item_created:
                cart_item.quantity += quantity
                cart_item.save()
            
            # Return updated cart
            cart_serializer = CartSerializer(cart)
            return APIResponse.success(
                message="Item added to cart", 
                data=cart_serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        
        return APIResponse.error(message="Validation Error", errors=serializer.errors)

class CartItemView(APIView):
    """Update or remove cart item"""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
        
        serializer = CartItemUpdateSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Return updated cart
            cart_serializer = CartSerializer(cart)
            return APIResponse.success(
                message="Cart item updated",
                data=cart_serializer.data
            )
        
        return APIResponse.error(message="Validation Error", errors=serializer.errors)

    def delete(self, request, pk):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
        cart_item.delete()
        
        # Return updated cart
        cart_serializer = CartSerializer(cart)
        return APIResponse.success(
            message="Item removed from cart",
            data=cart_serializer.data
        )
