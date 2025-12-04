from rest_framework import serializers
from .models import OrderGroup, Order, OrderItem
from apps.restaurants.serializers import RestaurantSerializer, MenuItemSerializer
from apps.locations.models import Address

class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.UUIDField()
    payment_method = serializers.CharField(max_length=20, default='CASH')

    def validate_address_id(self, value):
        if not Address.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid address ID")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_details = MenuItemSerializer(source='menu_item', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    restaurant_details = RestaurantSerializer(source='restaurant', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_group', 'restaurant', 'total_price', 'created_at', 'delivery_partner')

class OrderGroupSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(source='order_set', many=True, read_only=True)

    class Meta:
        model = OrderGroup
        fields = '__all__'
        read_only_fields = ('customer', 'created_at', 'status', 'total_price')
