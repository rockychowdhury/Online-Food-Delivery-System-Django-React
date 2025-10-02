from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with email and password"""
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        if not password:
            raise ValueError("Password is required for user creation")
        
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

class UserRoleManager(models.Manager):
    """Manager for UserRole model"""
    
    def assign_role(self, user, role):
        """Assign a role to user, deactivating any existing active role"""
        # Deactivate existing active roles
        self.filter(user=user, is_active=True).update(is_active=False)
        
        # Create new role assignment
        user_role = self.create(user=user, role=role, is_active=True)
        return user_role
    
    def get_active_role(self, user):
        """Get user's active role"""
        return self.filter(user=user, is_active=True).first()
