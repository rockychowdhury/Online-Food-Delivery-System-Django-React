from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from restaurants.models import Restaurant
from menu.models import FoodItem
from django.utils.translation import gettext_lazy as _
User = get_user_model()


class Cuisine(models.Model):
    """Model for cuisines (e.g., Italian, Chinese, Indian)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.URLField(max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = _('Cuisine')
        verbose_name_plural = _('Cuisines')
        ordering = ['name']
        
    def __str__(self):
        return self.name
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='reviews', 
                                    null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews', 
                                    null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at']
        
    def __str__(self):
        if self.food_item:
            return f"Review for {self.food_item.name} by {self.user.get_full_name() or self.user.username}"
        return f"Review for {self.restaurant.name} by {self.user.get_full_name() or self.user.username}"