from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_email
from .managers import UserManager,UserRoleManager
from django.conf import settings
from apps.common.mixins import BaseModel, UUIDMixin, TimestampMixin
from apps.common.utils.validators import phone_regex_validator
from django.contrib.auth import get_user_model

USER = get_user_model()

class User(AbstractUser, UUIDMixin, TimestampMixin):
    """Custom user model with email as username field"""
    
    email                   = models.EmailField(unique=True, validators=[validate_email], db_index=True, help_text="User's email address (used for login)")
    
    phone                   = models.CharField(validators=[phone_regex_validator], max_length=15, blank=True, null=True)
    

    date_of_birth           = models.DateField(blank=True, null=True)
    bio                     = models.TextField(max_length=500, blank=True, null=True)
    photoURL                = models.URLField(max_length=200, blank=True, null=True, default='https://i.ibb.co.com/3yv72K8q/chef-avatar-icon-vector-32077717.webp')


    is_phone_verified       = models.BooleanField(default=False)
    is_email_verified       = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email'], name='email_idx')
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    @property
    def is_verified(self):
        """Check if user has verified email or phone"""
        return self.is_email_verified or self.is_phone_verified

    def get_active_role(self):
        """Get the user's primary active role"""
        return self.user_roles.filter(is_active=True).first()
    
    def get_full_name(self):
        """Return the user's full name"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email.split('@')[0]


class Role(BaseModel):
    """Defines different roles in the system"""

    class RoleType(models.TextChoices):
        SYSTEM              = 'SYSTEM', 'System Level'
        RESTAURANT          = 'RESTAURANT', 'Restaurant Level'
        PLATFORM            = 'PLATFORM', 'Platform User'

    class RoleName(models.TextChoices):
        SUPER_ADMIN         = 'SUPER_ADMIN', 'Super Admin'
        # SYSTEM_STAFF        = 'SYSTEM_STAFF', 'System Staff'
        RESTAURANT_ADMIN    = 'RESTAURANT_ADMIN', 'Restaurant Admin'
        BRANCH_MANAGER      = 'BRANCH_MANAGER', 'Branch Manager'
        # BRANCH_STAFF        = 'BRANCH_STAFF', 'Branch Staff'
        CUSTOMER            = 'CUSTOMER', 'Customer'
        DELIVERY_PARTNER    = 'DELIVERY_PARTNER', 'Delivery Partner'

    name                    = models.CharField(max_length=50, choices=RoleName.choices, unique=True)
    role_type               = models.CharField(max_length=20, choices=RoleType.choices)
    description             = models.TextField(blank=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        indexes = [
            models.Index(fields=['name'], name='role_name_idx'),
            models.Index(fields=['role_type'], name='role_type_idx'),
        ]
    
    def __str__(self):
        return self.get_name_display()


class UserRole(BaseModel):
    """User role assignment model"""

    user                    = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='user_roles')
    role                    = models.ForeignKey(Role, on_delete=models.CASCADE)

    assigned_at             = models.DateTimeField(auto_now_add=True)
    expires_at              = models.DateTimeField(null=True, blank=True)

    objects = UserRoleManager()

    class Meta:
        db_table = 'user_roles'
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role'], 
                name='unique_user_role'
            ),
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_active=True),
                name='unique_active_role_per_user'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'is_active'], name='user_active_role_idx'),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role.name}"

class Permission(BaseModel):
    """Permission definitions"""
    
    RESOURCE_TYPES = [
        ('RESTAURANT', 'Restaurant'),
        ('BRANCH', 'Branch'),
        ('USER_PROFILE', 'User Profile'),
        ('MENU', 'Menu'),
        ('FOOD_ITEMS', 'Food Items'),
        ('ORDERS', 'Orders'),
        ('RATINGS', 'Ratings'),
        ('ADDRESS', 'Address'),
    ]
    
    ACTIONS = [
        ('CREATE', 'Create'),
        ('READ', 'Read'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    action = models.CharField(max_length=20, choices=ACTIONS)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ['resource_type', 'action']

    def __str__(self):
        return f"{self.resource_type}.{self.action}"


class RolePermission(BaseModel):
    """Many-to-many relationship between roles and permissions with access levels"""
    
    ACCESS_LEVELS = [
        ('FULL', 'Full Access'),
        ('LIMITED', 'Limited Access'),
        ('READ_ONLY', 'Read Only'),
        ('NONE', 'No Access'),
    ]
    
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVELS)
    conditions = models.JSONField(default=dict, blank=True)  # Store additional conditions

    class Meta:
        unique_together = ['role', 'permission']

    def __str__(self):
        return f"{self.role.name} - {self.permission.name} ({self.access_level})"