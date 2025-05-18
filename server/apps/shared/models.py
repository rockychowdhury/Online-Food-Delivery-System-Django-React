# from django.db import models
# from django.contrib.auth import get_user_model
# from django.core.validators import MinValueValidator, MaxValueValidator
# from restaurants.models import Restaurant
# from menu.models import FoodItem
# from django.utils.translation import gettext_lazy as _
# User = get_user_model()


# from django.contrib.gis.db import models as geoModels
# from django.contrib.gis.geos import Point
# from django.contrib.auth import get_user_model
# from django.core.validators import RegexValidator

# User = get_user_model()

# class BaseLocation(geoModels.Model):
#     address_line1 = models.CharField(max_length=255)
#     address_line2 = models.CharField(max_length=255, blank=True, null=True)
#     landmark = models.CharField(max_length=100, blank=True, null=True)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     postal_code = models.CharField(
#         max_length=20,
#         validators=[RegexValidator(r'^[0-9]+$', 'Only numeric characters are allowed.')]
#     )
#     country = models.CharField(max_length=100, default='YourDefaultCountry')

#     location = models.PointField(geography=True, srid=4326)
#     latitude = models.FloatField(blank=True, null=True)
#     longitude = models.FloatField(blank=True, null=True)
    
#     # Common metadata
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         abstract = True

#     def save(self, *args, **kwargs):
#         """Auto-populate PointField from lat/lng"""
#         if self.latitude and self.longitude and not self.location:
#             self.location = Point(float(self.longitude), float(self.latitude))
#         super().save(*args, **kwargs)






# class Cuisine(models.Model):
#     """Model for cuisines (e.g., Italian, Chinese, Indian)."""
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)
#     image = models.URLField(max_length=200, blank=True, null=True)
    
#     class Meta:
#         verbose_name = _('Cuisine')
#         verbose_name_plural = _('Cuisines')
#         ordering = ['name']
        
#     def __str__(self):
#         return self.name
    

# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
#     food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='reviews', 
#                                     null=True, blank=True)
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews', 
#                                     null=True, blank=True)
#     rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = _('Review')
#         verbose_name_plural = _('Reviews')
#         ordering = ['-created_at']
        
#     def __str__(self):
#         if self.food_item:
#             return f"Review for {self.food_item.name} by {self.user.get_full_name() or self.user.username}"
#         return f"Review for {self.restaurant.name} by {self.user.get_full_name() or self.user.username}"