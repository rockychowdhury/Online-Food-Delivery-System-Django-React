from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import OrderGroup, Order, OrderItem
from .serializers import OrderGroupSerializer, OrderSerializer, OrderItemSerializer, CheckoutSerializer
from apps.cart.models import Cart
from apps.delivery.models import DeliveryStatus
from apps.common.utils import APIResponse

class OrderGroupViewSet(viewsets.ModelViewSet):
    queryset = OrderGroup.objects.all()
    serializer_class = OrderGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderGroup.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user, status='PENDING', total_price=0)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error("Validation Error", serializer.errors)

        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return APIResponse.error("Cart is empty", status_code=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # 1. Create OrderGroup
            order_group = OrderGroup.objects.create(
                customer=request.user,
                status='PENDING',
                total_price=cart.total_price
            )

            # 2. Group items by restaurant
            items_by_restaurant = {}
            for item in cart.items.all():
                restaurant = item.menu_item.menu.branch.restaurant
                if restaurant not in items_by_restaurant:
                    items_by_restaurant[restaurant] = []
                items_by_restaurant[restaurant].append(item)

            # 3. Create Orders and OrderItems
            pending_status, _ = DeliveryStatus.objects.get_or_create(status='PENDING')
            
            for restaurant, items in items_by_restaurant.items():
                restaurant_total = sum(item.subtotal for item in items)
                order = Order.objects.create(
                    order_group=order_group,
                    restaurant=restaurant,
                    delivery_status=pending_status,
                    total_price=restaurant_total
                )
                
                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        menu_item=item.menu_item,
                        quantity=item.quantity,
                        price=item.menu_item.price
                    )

            # 4. Clear Cart
            cart.items.all().delete()

        return APIResponse.success("Order placed successfully", {'order_group_id': order_group.id}, status_code=status.HTTP_201_CREATED)

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff: # Admin
            return Order.objects.all()
        # Check if user is restaurant owner/manager (simplified check)
        # In a real scenario, we'd check against managed restaurants
        return Order.objects.filter(order_group__customer=user) | Order.objects.filter(restaurant__owner=user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        # Permission check: Only owner/manager/admin
        if request.user != order.restaurant.owner and not request.user.is_staff:
             return APIResponse.error("Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        
        status_name = request.data.get('status')
        if status_name:
            delivery_status, _ = DeliveryStatus.objects.get_or_create(status=status_name)
            order.delivery_status = delivery_status
            order.save()
            return APIResponse.success("Status updated")
        return APIResponse.error("Status required")

class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__order_group__customer=self.request.user)
