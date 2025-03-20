from django.contrib.auth import get_user_model
from django.db import models
from shared.models import Cuisine
from restaurants.models import Restaurant, Branch
from django.utils.translation import gettext_lazy as _
User = get_user_model()


class FoodCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='food_categories/', blank=True, null=True)
    
    class Meta:
        verbose_name = _('Food Category')
        verbose_name_plural = _('Food Categories')
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='menus', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)
    is_special = models.BooleanField(default=False, help_text="Is this a special/seasonal menu?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')
        ordering = ['restaurant', 'name']
        
    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"

class FoodItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, 
                                related_name='food_items', null=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, 
                                related_name='food_items', null=True, blank=True)
    image_url = models.URLField()
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    preparation_time = models.PositiveIntegerField(help_text="Preparation time in minutes", default=15)
    calories = models.PositiveIntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Food Item')
        verbose_name_plural = _('Food Items')
        ordering = ['menu', 'name']
        
    def __str__(self):
        return f"{self.name} - {self.menu.restaurant.name}"
