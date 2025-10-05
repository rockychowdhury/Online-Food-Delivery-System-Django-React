from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    logo = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"

class Menu(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cuisine = models.ForeignKey('Cuisine', on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
class Cuisine(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
