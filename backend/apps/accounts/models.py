from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, validate_email
from apps.common.models import TimestampedModel
from .managers import UserManager, AddressManager
import uuid

class User(AbstractUser):
    """Custom user model with email as the primary identifier"""
    
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email                   = models.EmailField(unique=True, validators=[validate_email], db_index=True)
    first_name              = models.CharField(max_length=30)
    last_name               = models.CharField(max_length=30)

    phone_regex             = RegexValidator( regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone                   = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)



    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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

# photoURL                = models.URLField( max_length=200, blank=True, null=True, default='https://i.ibb.co.com/3yv72K8q/chef-avatar-icon-vector-32077717.webp', validators=[validate_image_url] )


class Address(TimestampedModel):
    """User address model"""
    
    ADDRESS_TYPES = (
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home')
    
    # Address fields
    label = models.CharField(max_length=50, help_text="e.g., 'Home', 'Office'")
    street_address = models.CharField(max_length=255)
    apartment_number = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Bangladesh')
    
    # Location coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Additional fields
    landmark = models.CharField(max_length=255, blank=True)
    delivery_instructions = models.TextField(blank=True)
    
    # Status fields
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = AddressManager()
    
    class Meta:
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        indexes = [
            models.Index(fields=['user', 'is_default']),
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.label} - {self.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        """Override save to ensure only one default address per user"""
        if self.is_default:
            # Set all other addresses for this user to non-default
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
    
    @property
    def full_address(self):
        """Return formatted full address"""
        address_parts = [self.street_address]
        
        if self.apartment_number:
            address_parts.append(f"Apt {self.apartment_number}")
        
        address_parts.extend([self.city, self.state, self.postal_code])
        
        if self.country != 'Bangladesh':
            address_parts.append(self.country)
        
        return ', '.join(address_parts)