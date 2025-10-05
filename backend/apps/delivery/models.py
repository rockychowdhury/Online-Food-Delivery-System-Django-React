from django.db import models

class DeliveryPartner(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=30)
    rating = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)

class DeliveryStatus(models.Model):
    status = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

