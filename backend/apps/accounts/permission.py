# # permissions.py - Custom Permission Classes

# from rest_framework.permissions import BasePermission
# from rest_framework.exceptions import PermissionDenied
# from django.core.exceptions import ObjectDoesNotExist
# import logging

# logger = logging.getLogger(__name__)


# class RoleBasedPermission(BasePermission):
#     """
#     Base permission class for role-based access control
#     """
    
#     def has_permission(self, request, view):
#         """Check if user has permission to access the view"""
#         if not request.user or not request.user.is_authenticated:
#             return False
            
#         active_role = request.user.get_active_role()
#         if not active_role or not active_role.is_valid():
#             return False
            
#         return True

#     def has_object_permission(self, request, view, obj):
#         """Check if user has permission to access specific object"""
#         return self.has_permission(request, view)


# class ResourcePermission(RoleBasedPermission):
#     """
#     Permission class that checks specific resource permissions
#     Usage: Set resource_name and required_actions in view
#     """
    
#     def has_permission(self, request, view):
#         if not super().has_permission(request, view):
#             return False
            
#         # Get resource and action from view
#         resource_name = getattr(view, 'resource_name', None)
#         if not resource_name:
#             logger.warning(f"No resource_name defined for view {view.__class__.__name__}")
#             return False
            
#         # Map HTTP methods to actions
#         action_map = {
#             'GET': 'READ',
#             'POST': 'CREATE',
#             'PUT': 'UPDATE',
#             'PATCH': 'UPDATE',
#             'DELETE': 'DELETE',
#         }
        
#         action = action_map.get(request.method)
#         if not action:
#             return False
            
#         # Check if user has permission for this resource/action
#         return self._check_resource_permission(request.user, resource_name, action)
    
#     def has_object_permission(self, request, view, obj):
#         """Check object-level permissions with scoping"""
#         if not self.has_permission(request, view):
#             return False
            
#         # Check resource scoping
#         return self._check_resource_scoping(request.user, obj)
    
#     def _check_resource_permission(self, user, resource_name, action):
#         """Check if user's role has permission for resource/action"""
#         active_role = user.get_active_role()
#         if not active_role:
#             return False
            
#         try:
#             from .models import Permission, RolePermission
            
#             permission = Permission.objects.get(
#                 resource_type=resource_name,
#                 action=action,
#                 is_active=True
#             )
            
#             role_permission = RolePermission.objects.get(
#                 role=active_role.role,
#                 permission=permission,
#                 is_active=True
#             )
            
#             return role_permission.access_level in ['FULL', 'LIMITED']
            
#         except (Permission.DoesNotExist, RolePermission.DoesNotExist):
#             return False
    
#     def _check_resource_scoping(self, user, obj):
#         """Check if user has access to specific object based on scoping"""
#         active_role = user.get_active_role()
#         if not active_role:
#             return False
            
#         role_name = active_role.role.name
        
#         # Super admin and system staff have access to everything
#         if role_name in ['SUPER_ADMIN', 'SYSTEM_STAFF']:
#             return True
            
#         # Check scoping based on object type
#         if hasattr(obj, 'restaurant'):
#             # Object belongs to a restaurant
#             restaurant = obj.restaurant
#             return active_role.scoped_restaurants.filter(id=restaurant.id).exists()
#         elif hasattr(obj, 'owner') and obj.owner == user:
#             # User owns the object
#             return True
#         elif obj.__class__.__name__ == 'Restaurant':
#             # Object is a restaurant
#             return active_role.scoped_restaurants.filter(id=obj.id).exists()
#         elif obj.__class__.__name__ == 'Branch':
#             # Object is a branch
#             return (
#                 active_role.scoped_branches.filter(id=obj.id).exists() or
#                 active_role.scoped_restaurants.filter(id=obj.restaurant.id).exists()
#             )
            
#         return False


# class RestaurantScopedPermission(ResourcePermission):
#     """
#     Permission class for restaurant-scoped resources
#     """
    
#     def has_object_permission(self, request, view, obj):
#         if not super().has_object_permission(request, view, obj):
#             return False
            
#         active_role = request.user.get_active_role()
#         if not active_role:
#             return False
            
#         # Restaurant owners can only access their own restaurants
#         if active_role.role.name == 'RESTAURANT_OWNER':
#             if hasattr(obj, 'restaurant'):
#                 return obj.restaurant.owner == request.user
#             elif obj.__class__.__name__ == 'Restaurant':
#                 return obj.owner == request.user
                
#         return True


# class BranchScopedPermission(ResourcePermission):
#     """
#     Permission class for branch-scoped resources
#     """
    
#     def has_object_permission(self, request, view, obj):
#         if not super().has_object_permission(request, view, obj):
#             return False
            
#         active_role = request.user.get_active_role()
#         if not active_role:
#             return False
            
#         # Branch managers can only access their managed branches
#         if active_role.role.name == 'BRANCH_MANAGER':
#             if hasattr(obj, 'branch'):
#                 return obj.branch.manager == request.user
#             elif obj.__class__.__name__ == 'Branch':
#                 return obj.manager == request.user
                
#         return True


# class CustomerPermission(RoleBasedPermission):
#     """
#     Permission class for customer-specific resources
#     """
    
#     def has_permission(self, request, view):
#         if not super().has_permission(request, view):
#             return False
            
#         active_role = request.user.get_active_role()
#         return active_role and active_role.role.name == 'CUSTOMER'
    
#     def has_object_permission(self, request, view, obj):
#         if not self.has_permission(request, view):
#             return False
            
#         # Customers can only access their own resources
#         if hasattr(obj, 'customer'):
#             return obj.customer == request.user
#         elif hasattr(obj, 'user'):
#             return obj.user == request.user
            
#         return False


# class DeliveryPartnerPermission(RoleBasedPermission):
#     """
#     Permission class for delivery partner resources
#     """
    
#     def has_permission(self, request, view):
#         if not super().has_permission(request, view):
#             return False
            
#         active_role = request.user.get_active_role()
#         return active_role and active_role.role.name == 'DELIVERY_PARTNER'
    
#     def has_object_permission(self, request, view, obj):
#         if not self.has_permission(request, view):
#             return False
            
#         # Delivery partners can only access assigned orders
#         if obj.__class__.__name__ == 'Order':
#             return obj.delivery_partner == request.user
            
#         return False


from rest_framework.permissions import BasePermission
from .models import RolePermission

class IsAuthenticatedAndVerified(BasePermission):
    """Allows access only to authenticated and verified users."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_verified)

class HasModelPermission(BasePermission):
    """Checks model-level permissions for the user's role."""
    def has_permission(self, request, view):
        user_role = request.user.get_active_role()
        if not user_role:
            return False
        resource = getattr(view, 'permission_resource', None)
        action = self.get_action(request)
        return self.check_permission(user_role, resource, action)
    
    def get_action(self, request):
        if request.method == 'POST':
            return 'CREATE'
        elif request.method in ['PUT', 'PATCH']:
            return 'UPDATE'
        elif request.method == 'DELETE':
            return 'DELETE'
        return 'READ'

    def check_permission(self, role, resource, action):
        # Query on RolePermission model to see if this role has access to the resource/action
        perm = RolePermission.objects.filter(
            role=role,
            permission__resource_type=resource,
            permission__action=action,
        ).first()
        return perm and perm.access_level in ['FULL', 'LIMITED', 'READ_ONLY']

class IsObjectOwnerOrRolePermission(BasePermission):
    """
    Object-level permission: check user ownership or explicit permission.
    """
    def has_object_permission(self, request, view, obj):
        user_role = request.user.get_active_role()
        resource = getattr(view, 'permission_resource', None)
        action = self.get_action(request)
        # Ownership check
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True
        # Role-based object access
        perm = RolePermission.objects.filter(
            role=user_role,
            permission__resource_type=resource,
            permission__action=action,
        ).first()
        return perm and perm.access_level in ['FULL', 'LIMITED']

    def get_action(self, request):
        if request.method == 'POST':
            return 'CREATE'
        elif request.method in ['PUT', 'PATCH']:
            return 'UPDATE'
        elif request.method == 'DELETE':
            return 'DELETE'
        return 'READ'
