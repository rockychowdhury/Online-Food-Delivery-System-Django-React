from django.db import models
from .managers import AddressManager
import uuid
from django.conf import settings

class Country(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country_name            = models.CharField(max_length=100, unique=True)
    country_code            = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "countries"
        verbose_name = "Country"
        verbose_name_plural = "Countries"
    
    def __str__(self):
        return f"{self.country_name} ({self.country_code})"

class Address(models.Model):
    """User address model"""
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    street_address          = models.CharField(max_length=255)
    apartment_number        = models.CharField(max_length=50, blank=True)

    city                    = models.CharField(max_length=100)
    state                   = models.CharField(max_length=100)
    postal_code             = models.CharField(max_length=20)
    country                 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='addresses')
    
    # Location coordinates
    latitude                = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude               = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Additional fields
    delivery_instructions   = models.TextField(blank=True)

    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)

    objects = AddressManager()
    
    class Meta:
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
    
    def __str__(self):
        return self.full_address
    
    @property
    def full_address(self):
        """Return full address"""
        address_lines = []
    
        # Street address line
        street_line = self.street_address
        if self.apartment_number:
            street_line += f", {self.apartment_number}"
        address_lines.append(street_line)
    
        # City/State/Zip line
        locality_line = f"{self.city}, {self.state}"
        if self.postal_code:
            locality_line += f" {self.postal_code}"
        address_lines.append(locality_line)
        
        if hasattr(self.country, 'country_name'):
            country_name = self.country.country_name
            address_lines.append(country_name)
        return ', '.join(address_lines)

class UserAddress(models.Model):
    """Mapping between users and their addresses"""
    class AddressType(models.TextChoices):
        HOME                = 'home', 'Home'
        WORK                = 'work', 'Work'
        OTHER               = 'other', 'Other'


    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    address                 = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='user_addresses')
    address_type            = models.CharField(max_length=10, choices=AddressType.choices, default='home')
    is_active               = models.BooleanField(default=True)
    is_default              = models.BooleanField(default=False)
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_addresses'
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_default=True, is_active=True),
                name='unique_default_address_per_user'
            )
        ]