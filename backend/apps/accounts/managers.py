from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Q

class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user"""
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_email_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
            
        return self.create_user(email, password, **extra_fields)
    def active_users(self):
        """Get all active users"""
        return self.filter(is_active=True)
    
    def verified_users(self):
        """Get all verified users"""
        return self.filter(
            Q(is_email_verified=True) | Q(is_phone_verified=True),
            is_active=True
        )


class UserRoleManager(models.Manager):
    """Manager for UserRole model"""
    
    def assign_role(self, user, role, expires_at=None):
        """
        Assign a role to user, deactivating any existing active role.
        Returns the newly created UserRole instance.
        """

        # Deactivate existing active roles
        self.filter(user=user, is_active=True).update(is_active=False)
        
        # Create new role assignment
        user_role = self.create(user=user, role=role, is_active=True, expires_at=expires_at)
        return user_role
    
    def get_active_role(self, user):
        """Get user's active role"""
        return self.filter(user=user, is_active=True).first()
    
    def get_user_roles_history(self, user):
        """Get all roles ever assigned to user"""
        return self.filter(user=user).order_by('-assigned_at')
    
    def users_with_role(self, role_name):
        """Get all users with a specific active role"""
        return self.filter(
            role__name=role_name, 
            is_active=True
        ).select_related('user', 'role')
    