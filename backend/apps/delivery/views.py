from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DeliveryPartner, DeliveryStatus
from .serializers import DeliveryPartnerSerializer, DeliveryStatusSerializer
from apps.orders.models import Order
from apps.common.utils import APIResponse

class DeliveryPartnerViewSet(viewsets.ModelViewSet):
    queryset = DeliveryPartner.objects.all()
    serializer_class = DeliveryPartnerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def available_orders(self, request):
        # Orders ready for pickup (e.g., status='READY_FOR_PICKUP' or 'PENDING' for now)
        # And not yet assigned to a partner
        pending_status = DeliveryStatus.objects.filter(status='PENDING').first()
        if not pending_status:
             return APIResponse.success("No orders available", [])
             
        orders = Order.objects.filter(delivery_status=pending_status, delivery_partner__isnull=True)
        # In real app, filter by location
        data = [{'id': o.id, 'restaurant': o.restaurant.name, 'total': o.total_price} for o in orders]
        return APIResponse.success("Available orders", data)

    @action(detail=False, methods=['post'], url_path='orders/(?P<pk>[^/.]+)/claim')
    def claim_order(self, request, pk=None):
        try:
            partner = DeliveryPartner.objects.get(user=request.user)
        except DeliveryPartner.DoesNotExist:
            return APIResponse.error("User is not a delivery partner", status_code=status.HTTP_403_FORBIDDEN)

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return APIResponse.error("Order not found", status_code=status.HTTP_404_NOT_FOUND)

        if order.delivery_partner:
            return APIResponse.error("Order already claimed", status_code=status.HTTP_400_BAD_REQUEST)

        order.delivery_partner = partner
        order.save()
        return APIResponse.success("Order claimed successfully")

    @action(detail=False, methods=['post'], url_path='orders/(?P<pk>[^/.]+)/update-status')
    def update_status(self, request, pk=None):
        try:
            partner = DeliveryPartner.objects.get(user=request.user)
        except DeliveryPartner.DoesNotExist:
            return APIResponse.error("User is not a delivery partner", status_code=status.HTTP_403_FORBIDDEN)

        try:
            order = Order.objects.get(pk=pk, delivery_partner=partner)
        except Order.DoesNotExist:
            return APIResponse.error("Order not found or not assigned to you", status_code=status.HTTP_404_NOT_FOUND)

        status_name = request.data.get('status')
        if status_name:
            delivery_status, _ = DeliveryStatus.objects.get_or_create(status=status_name)
            order.delivery_status = delivery_status
            order.save()
            return APIResponse.success("Status updated")
        return APIResponse.error("Status required")

class DeliveryStatusViewSet(viewsets.ModelViewSet):
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
