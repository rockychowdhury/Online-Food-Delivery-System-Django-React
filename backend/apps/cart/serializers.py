from rest_framework import serializers
from .models import Cart, CartItem
from apps.restaurants.models import MenuItem

class CartItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.ReadOnlyField(source='menu_item.name')
    menu_item_price = serializers.ReadOnlyField(source='menu_item.price')
    restaurant_name = serializers.ReadOnlyField(source='menu_item.menu.branch.restaurant.name')
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'menu_item', 'menu_item_name', 'menu_item_price', 'restaurant_name', 'quantity', 'subtotal']
        read_only_fields = ['id', 'menu_item_name', 'menu_item_price', 'restaurant_name', 'subtotal']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'updated_at']
        read_only_fields = ['id', 'items', 'total_price', 'updated_at']

class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['menu_item', 'quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value
