from django.db import models
from apps.common.mixins import BaseModel
from .managers import AddressManager
from django.contrib.auth import get_user_model

User = get_user_model()

class Country(BaseModel):
    """Country model for address management"""
    name                    = models.CharField(max_length=100, unique=True)
    code                    = models.CharField(max_length=10, unique=True)
    currency                = models.CharField(max_length=10)
    timezone                = models.CharField(max_length=50)

    class Meta:
        db_table = "countries"
        verbose_name = "Country"
        verbose_name_plural = "Countries"

        indexes = [
            models.Index(fields=['code'], name='code_idx'),
        ]
    def __str__(self):
        return f"{self.name} ({self.code})"

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)


class Address(BaseModel):
    """Address model for location management"""

    street_address          = models.CharField(max_length=255)
    apartment_number        = models.CharField(max_length=50, blank=True)

    city                    = models.ForeignKey(City, on_delete=models.PROTECT, related_name='addresses')
    state                   = models.CharField(max_length=100)
    postal_code             = models.CharField(max_length=20)
    
    # Location coordinates
    latitude                = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,help_text="Latitude coordinate for precise location")
    longitude               = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,help_text="Latitude coordinate for precise location")
    
    # Additional fields
    delivery_instructions   = models.TextField(blank=True, help_text="Special delivery instructions  this address")

    objects = AddressManager()
    
    class Meta:
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        indexes = [
            models.Index(fields=['city', 'state'], name='address_city_state_idx'),
            models.Index(fields=['postal_code'], name='address_postal_code_idx'),
        ]
    def __str__(self):
        return self.full_address
    
    @property
    def full_address(self):
        """Return formatted full address"""
        address_parts = []
        
        # Street address
        street_line = self.street_address
        if self.apartment_number:
            street_line += f", Apt {self.apartment_number}"
        address_parts.append(street_line)
        
        # City, State Postal Code
        locality_line = f"{self.city.name}, {self.state}"
        if self.postal_code:
            locality_line += f" {self.postal_code}"
        address_parts.append(locality_line)
        
        # Country
        if self.city.country:
            address_parts.append(self.city.country.name)
        
        return ', '.join(address_parts)

class UserAddress(BaseModel):
    """Mapping between users and their addresses"""

    class AddressType(models.TextChoices):
        HOME                = 'home', 'Home'
        WORK                = 'work', 'Work'
        OTHER               = 'other', 'Other'

    user                    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address                 = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='user_addresses')
    address_type            = models.CharField(max_length=10, choices=AddressType.choices, default=AddressType.HOME)
    label                   = models.CharField(max_length=50, blank=True, help_text="Custom label for this address (e.g., 'Mom's House')"
    )
    is_default              = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user_addresses'
        verbose_name = 'User Address'
        verbose_name_plural = 'User Addresses'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'address'],
                name='unique_user_address'
            ),
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_default=True, is_active=True),
                name='unique_default_address_per_user'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'is_active'], name='user_address_active_idx'),
            models.Index(fields=['user', 'is_default'], name='user_address_default_idx'),
        ]
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.address_type.title()}: {self.address.city}"
    
    def save(self, *args, **kwargs):
        """Override save to handle default address logic"""
        if self.is_default:
            # Remove default from other addresses
            UserAddress.objects.filter(
                user=self.user, 
                is_default=True, 
                is_active=True
            ).exclude(id=self.id).update(is_default=False)
        
        super().save(*args, **kwargs)