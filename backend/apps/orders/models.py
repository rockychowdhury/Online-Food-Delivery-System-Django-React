from django.db import models
from django.conf import settings
from apps.restaurants.models import Restaurant, MenuItem

class OrderGroup(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)
    payment = models.ForeignKey('payments.Payment', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"OrderGroup {self.id} by {self.customer}"

class Order(models.Model):
    order_group = models.ForeignKey(OrderGroup, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    delivery_status = models.ForeignKey('delivery.DeliveryStatus', on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_partner = models.ForeignKey('delivery.DeliveryPartner', on_delete=models.SET_NULL, null=True, blank=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    special_instructions = models.TextField(blank=True, null=True)
