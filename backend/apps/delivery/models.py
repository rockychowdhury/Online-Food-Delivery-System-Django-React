from django.db import models
from django.conf import settings

class DeliveryPartner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=30)
    average_rating = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)

class DeliveryStatus(models.Model):
    status = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

