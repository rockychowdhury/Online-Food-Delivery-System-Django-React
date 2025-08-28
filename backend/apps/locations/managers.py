from django.db import models


class AddressManager(models.Manager):
    def get_user_addresses(self, user):
        """Get all addresses for a specific user"""
        return self.filter(user=user, is_active=True)
    
    def get_default_address(self, user):
        """Get user's default address"""
        try:
            return self.get(user=user, is_default=True, is_active=True)
        except self.model.DoesNotExist:
            return None