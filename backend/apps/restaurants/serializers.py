from rest_framework import serializers
from .models import Restaurant, Branch, Menu, MenuItem, Cuisine, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    cuisine = CuisineSerializer(read_only=True)
    cuisine_id = serializers.PrimaryKeyRelatedField(
        queryset=Cuisine.objects.all(), source='cuisine', write_only=True, allow_null=True
    )
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, allow_null=True
    )

    class Meta:
        model = MenuItem
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(source='menuitem_set', many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(source='branch_set', many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'is_approved')

class RestaurantApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['is_approved', 'is_active']
