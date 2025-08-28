from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, validate_email
from .managers import UserManager,UserRoleManager, AddressManager
import uuid
from django.conf import settings


class User(AbstractUser):

    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email                   = models.EmailField(unique=True, validators=[validate_email], db_index=True)

    phone_regex             = RegexValidator( regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone                   = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    

    date_of_birth           = models.DateField(blank=True, null=True)
    bio                     = models.TextField(max_length=200, blank=True, null=True)
    photoURL                = models.URLField(max_length=200, blank=True, null=True, default='https://i.ibb.co.com/3yv72K8q/chef-avatar-icon-vector-32077717.webp')


    is_phone_verified       = models.BooleanField(default=False)
    is_email_verified       = models.BooleanField(default=False)

    is_staff                = models.BooleanField(default=False)
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_active_role(self):
        """Get the user's primary active role"""
        return self.user_role.filter(is_active=True).first()
    
    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip()


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


class UserRole(models.Model):
    
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_role')
    role                    = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active               = models.BooleanField(default=True)

    assigned_at             = models.DateTimeField(auto_now_add=True)
    expires_at              = models.DateTimeField(null=True, blank=True)
    updated_at              = models.DateTimeField(auto_now=True)

    objects = UserRoleManager()

    class Meta:
        db_table = 'user_roles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        unique_together = ('user', 'role')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role.name}"
