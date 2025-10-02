from django.db import models
from django.db.models import Q


class AddressManager(models.Manager):
    """Manager for Address model"""
    
    def active_addresses(self):
        """Get all active addresses"""
        return self.filter(is_active=True)
    
    def get_user_addresses(self, user):
        """Get all addresses for a specific user through UserAddress"""
        return self.filter(
            user_addresses__user=user, 
            user_addresses__is_active=True,
            is_active=True
        ).distinct()
    
    def get_default_address(self, user):
        """Get user's default address"""
        try:
            user_address = self.get(
                user_addresses__user=user,
                user_addresses__is_default=True,
                user_addresses__is_active=True,
                is_active=True
            )
            return user_address
        except self.model.DoesNotExist:
            return None
    
    def search_by_location(self, city=None, state=None, postal_code=None):
        """Search addresses by location parameters"""
        queryset = self.active_addresses()
        
        if city:
            queryset = queryset.filter(city__icontains=city)
        if state:
            queryset = queryset.filter(state__icontains=state)
        if postal_code:
            queryset = queryset.filter(postal_code=postal_code)
            
        return queryset