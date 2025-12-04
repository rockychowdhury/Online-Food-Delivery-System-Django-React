from django.db import models
from django.conf import settings


class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    logo = models.URLField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    class BranchType(models.TextChoices):
        DINE_IN = 'DINE_IN', 'Dine-in'
        DELIVERY = 'DELIVERY', 'Delivery'
        PICKUP = 'PICKUP', 'Pickup'

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)
    branch_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='managed_branches')
    address = models.ForeignKey('locations.Address', on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    phone = models.CharField(max_length=15)
    branch_type = models.CharField(max_length=20, choices=BranchType.choices, default=BranchType.DELIVERY)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Menu(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cuisine = models.ForeignKey('Cuisine', on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True)
    image = models.URLField(blank=True, null=True)
    
    # Detailed info
    ingredients = models.TextField(blank=True, help_text="Comma separated list of ingredients")
    allergens = models.TextField(blank=True, help_text="Comma separated list of allergens")
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class Cuisine(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
