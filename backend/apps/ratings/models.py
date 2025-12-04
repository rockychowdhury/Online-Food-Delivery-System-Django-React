from django.db import models
from django.conf import settings
from apps.orders.models import Order

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey('delivery.DeliveryPartner', on_delete=models.SET_NULL, null=True)
    score = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
