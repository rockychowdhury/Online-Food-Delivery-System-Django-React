from django.db import models
import uuid


class TimestampMixin(models.Model):
    """Abstract model mixin for created_at and updated_at fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Abstract model mixin for UUID primary key"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """Abstract model mixin for soft delete functionality"""
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        """Mark object as deleted"""
        from django.utils import timezone
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()


class BaseModel(UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Base model with common fields for all models"""
    class Meta:
        abstract = True