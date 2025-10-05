from django.db import models
from apps.orders.models import Orders

class Rating(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey('DeliveryPartner', on_delete=models.SET_NULL, null=True)
    score = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
