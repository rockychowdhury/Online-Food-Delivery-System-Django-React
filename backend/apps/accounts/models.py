from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, validate_email
from .managers import UserManager, AddressManager
import uuid
from django.conf import settings


class User(AbstractUser):
    """Custom user model"""
    
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email                   = models.EmailField(unique=True, validators=[validate_email], db_index=True)

    phone_regex             = RegexValidator( regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone                   = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    
    is_phone_verified       = models.BooleanField(default=False)
    is_email_verified       = models.BooleanField(default=False)

    is_staff                = models.BooleanField(default=False)
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        """Return the user's short name"""
        return self.first_name


class Role(models.Model):
    """Defines different roles in the system"""

    class RoleType(models.TextChoices):
        SYSTEM              = 'SYSTEM', 'System Level'
        RESTAURANT          = 'RESTAURANT', 'Restaurant Level'
        PLATFORM            = 'PLATFORM', 'Platform User'

    class RoleName(models.TextChoices):
        SUPER_ADMIN         = 'SUPER_ADMIN', 'Super Admin'
        SYSTEM_STAFF        = 'SYSTEM_STAFF', 'System Staff'
        RESTAURANT_OWNER    = 'RESTAURANT_OWNER', 'Restaurant Owner'
        BRANCH_MANAGER      = 'BRANCH_MANAGER', 'Branch Manager'
        BRANCH_STAFF        = 'BRANCH_STAFF', 'Branch Staff'
        CUSTOMER            = 'CUSTOMER', 'Customer'
        DELIVERY_PARTNER    = 'DELIVERY_PARTNER', 'Delivery Partner'

    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name                    = models.CharField(max_length=50, choices=RoleName.choices, unique=True)
    role_type               = models.CharField(max_length=20, choices=RoleType.choices)
    description             = models.TextField(blank=True)
    is_active               = models.BooleanField(default=True)
    created_at              = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.get_name_display()


class UserProfile(models.Model):
    """UserRole model to extend user with roles and additional info"""
    
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user                    = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role                    = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_profiles")
    bio                     = models.TextField(max_length=200, blank=True, null=True)
    photoURL                = models.URLField(max_length=200, blank=True, null=True, default='https://i.ibb.co.com/3yv72K8q/chef-avatar-icon-vector-32077717.webp')

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        unique_together = ('user', 'role')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role.name}"


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
