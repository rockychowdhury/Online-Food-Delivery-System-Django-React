# from django.contrib.auth import get_user_model
# from django.db import models
# from shared.models import Cuisine
# from django.db import models

# from django.utils.translation import gettext_lazy as _

# User = get_user_model()


# class RestaurantCategory(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)
#     image_url = models.URLField(blank=True, null=True)
    
#     class Meta:
#         verbose_name = _('Restaurant Category')
#         verbose_name_plural = _('Restaurant Categories')
#         ordering = ['name']
        
#     def __str__(self):
#         return self.name


# class Restaurant(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     logo = models.URLField(blank=True, null=True) 
#     banner_image = models.URLField(blank=True, null=True) 
#     phone_number = models.CharField(max_length=15)
#     email = models.EmailField()
#     website = models.URLField(blank=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     avg_preparation_time = models.PositiveIntegerField(help_text="Average preparation time in minutes", default=30)
#     categories = models.ManyToManyField(RestaurantCategory, related_name='restaurants')
#     cuisines = models.ManyToManyField(Cuisine, related_name='restaurants')
    
#     class Meta:
#         verbose_name = _('Restaurant')
#         verbose_name_plural = _('Restaurants')
#         ordering = ['name']
        
#     def __str__(self):
#         return self.name


# class Location(models.Model):
#     address_line1 = models.CharField(max_length=255)
#     address_line2 = models.CharField(max_length=255, blank=True)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=20)
#     country = models.CharField(max_length=100)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)
#     service_radius = models.DecimalField(max_digits=5, decimal_places=2, 
#                                         help_text="Service radius in kilometers")
    
#     class Meta:
#         verbose_name = _('Location')
#         verbose_name_plural = _('Locations')
        
#     def __str__(self):
#         return f"{self.address_line1}, {self.city}, {self.postal_code}"


# class Branch(models.Model):
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='branches')
#     name = models.CharField(max_length=255)
#     location = models.OneToOneField(Location, on_delete=models.CASCADE, related_name='branch')
#     manager = models.OneToOneField(User,on_delete=models.CASCADE, related_name="branch")
#     contact_number = models.CharField(max_length=15)
#     is_active = models.BooleanField(default=True)
#     opening_time = models.TimeField()
#     closing_time = models.TimeField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = _('Branch')
#         verbose_name_plural = _('Branches')
#         ordering = ['restaurant', 'name']
        
#     def __str__(self):
#         return f"{self.restaurant.name} - {self.name}"


# # class Payment(models.Model):
# #     """Model for payment information."""
# #     PAYMENT_METHOD_CHOICES = [
# #         ('credit_card', 'Credit Card'),
# #         ('debit_card', 'Debit Card'),
# #         ('cash', 'Cash on Delivery'),
# #         ('digital_wallet', 'Digital Wallet'),
# #         ('bank_transfer', 'Bank Transfer'),
# #     ]
    
# #     STATUS_CHOICES = [
# #         ('pending', 'Pending'),
# #         ('completed', 'Completed'),
# #         ('failed', 'Failed'),
# #         ('refunded', 'Refunded'),
# #     ]
    
# #     order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
# #     amount = models.DecimalField(max_digits=10, decimal_places=2)
# #     payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
# #     transaction_id = models.CharField(max_length=255, blank=True)
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
# #     payment_date = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)
    
# #     class Meta:
# #         verbose_name = _('Payment')
# #         verbose_name_plural = _('Payments')
        
# #     def __str__(self):
# #         return f"Payment for Order #{self.order.id} - {self.amount}"


# # class Coupon(models.Model):
# #     """Model for discount coupons."""
# #     DISCOUNT_TYPE_CHOICES = [
# #         ('percentage', 'Percentage'),
# #         ('fixed', 'Fixed Amount'),
# #     ]
    
# #     code = models.CharField(max_length=50, unique=True)
# #     description = models.TextField()
# #     discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
# #     discount_value = models.DecimalField(max_digits=10, decimal_places=2)
# #     min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
# #     valid_from = models.DateTimeField()
# #     valid_to = models.DateTimeField()
# #     is_active = models.BooleanField(default=True)
# #     max_uses = models.PositiveIntegerField(default=0, help_text="0 means unlimited uses")
# #     current_uses = models.PositiveIntegerField(default=0)
# #     restaurants = models.ManyToManyField(Restaurant, related_name='coupons', blank=True)
    
# #     class Meta:
# #         verbose_name = _('Coupon')
# #         verbose_name_plural = _('Coupons')
        
# #     def __str__(self):
# #         return self.code
    
# #     @property
# #     def is_valid(self):
# #         """Check if the coupon is currently valid."""
# #         from django.utils import timezone
# #         now = timezone.now()
# #         return (
# #             self.is_active and
# #             self.valid_from <= now and
# #             self.valid_to >= now and
# #             (self.max_uses == 0 or self.current_uses < self.max_uses)
# #         )


# # class CartItem(models.Model):
# #     """Model for items in a user's shopping cart."""
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
# #     food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
# #     quantity = models.PositiveIntegerField(default=1)
# #     special_instructions = models.TextField(blank=True)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)
    
# #     class Meta:
# #         verbose_name = _('Cart Item')
# #         verbose_name_plural = _('Cart Items')
# #         unique_together = ['user', 'food_item']
        
# #     def __str__(self):
# #         return f"{self.quantity} x {self.food_item.name} in {self.user.get_full_name() or self.user.username}'s cart"
    
# #     @property
# #     def total_price(self):
# #         """Calculate the total price for this cart item."""
# #         return self.food_item.discounted_price * self.quantity


# # class Favorite(models.Model):
# #     """Model for user favorites (restaurants or food items)."""
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
# #     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorited_by',
# #                                   null=True, blank=True)
# #     food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='favorited_by',
# #                                  null=True, blank=True)
# #     created_at = models.DateTimeField(auto_now_add=True)
    
# #     class Meta:
# #         verbose_name = _('Favorite')
# #         verbose_name_plural = _('Favorites')
# #         constraints = [
# #             models.UniqueConstraint(
# #                 fields=['user', 'restaurant'],
# #                 condition=models.Q(restaurant__isnull=False),
# #                 name='unique_user_restaurant_favorite'
# #             ),
# #             models.UniqueConstraint(
# #                 fields=['user', 'food_item'],
# #                 condition=models.Q(food_item__isnull=False),
# #                 name='unique_user_fooditem_favorite'
# #             ),
# #             models.CheckConstraint(
# #                 check=(
# #                     models.Q(food_item__isnull=False, restaurant__isnull=True) | 
# #                     models.Q(food_item__isnull=True, restaurant__isnull=False)
# #                 ),
# #                 name='favorite_either_food_or_restaurant'
# #             ),
# #         ]
        
# #     def __str__(self):
# #         if self.restaurant:
# #             return f"{self.user.get_full_name() or self.user.username} favorites {self.restaurant.name}"
# #         return f"{self.user.get_full_name() or self.user.username} favorites {self.food_item.name}"


# # class Notification(models.Model):
#     """Model for user notifications."""
#     NOTIFICATION_TYPES = [
#         ('order_status', 'Order Status'),
#         ('promotion', 'Promotion'),
#         ('system', 'System'),
#     ]
    
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
#     title = models.CharField(max_length=255)
#     message = models.TextField()
#     notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         verbose_name = _('Notification')
#         verbose_name_plural = _('Notifications')
#         ordering = ['-created_at']
        
#     def __str__(self):
#         return f"{self.title} - {self.user.get_full_name() or self.user.username}"