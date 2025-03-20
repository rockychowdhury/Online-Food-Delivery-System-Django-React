from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _





class UserManager(BaseUserManager):
    def create_user(self, email, password = None, **kwargs):
        if not email:
            raise ValueError('Email is Required')

        email = self.normalize_email(email)
        kwargs.setdefault('role', User.UserRole.GUEST)
        user = self.model(email=email,**kwargs)
        
        if password:
            user.set_password(password)
        else:
            raise ValueError("Password is required for user creation.")
        
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email, password=None, **kwargs):
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)
        kwargs.setdefault('role', User.UserRole.ADMIN)
        if not kwargs.get('is_staff') or not kwargs.get('is_superuser'):
            raise ValueError("Superuser must have is_staff=True and is_superuser=True.")
        
        user = self.create_user(email=email,password=password,**kwargs)
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    class UserRole(models.TextChoices):
        ADMIN                   = 'admin', 'Admin'
        CUSTOMER               = 'customer','Customer'
        OWNER                 = 'owner', 'Owner'
        GUEST                   = 'guest', 'Guest'

    email                   = models.EmailField(unique=True)
    first_name              = models.CharField(max_length=50)
    last_name               = models.CharField(max_length=50)
    phone_number            = models.CharField(max_length=15, blank=True, null=True)
    photoURL                = models.URLField(max_length=200, blank=True, null=True,default='https://i.ibb.co.com/3yv72K8q/chef-avatar-icon-vector-32077717.webp')
    bio                     = models.TextField(max_length=200, blank=True, null=True)
    role                    = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.GUEST)
    
    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)
    date_joined                 = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD              = 'email'
    REQUIRED_FIELDS             = ['first_name', 'last_name']


    class Meta:
        verbose_name            ='User'
        verbose_name_plural     = 'Users'
    
    def __str__(self) -> str:
        return f"{self.email} ({self.role})"
    
    def save(self, *args, **kwargs):
        if not self.role:
            self.role = self.UserRole.GUEST
        return super().save(*args, **kwargs)


    @property
    def is_customer(self):
        return self.role == 'customer'
    
    @property
    def is_owner(self):
        return self.role == 'owner'

    @property
    def is_admin(self):
        return self.role == 'admin'
    

class Address(models.Model):
    ADDRESS_TYPES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        
    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.postal_code}"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

