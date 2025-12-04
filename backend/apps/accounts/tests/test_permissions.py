from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import Role, UserRole, Permission, RolePermission
from apps.common.permissions import IsAuthenticatedAndVerified, HasModelPermission

User = get_user_model()

class PermissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='StrongPassword123!',
            is_email_verified=True
        )
        
        self.role = Role.objects.create(
            name=Role.RoleName.RESTAURANT_ADMIN,
            role_type=Role.RoleType.RESTAURANT
        )
        
        self.permission = Permission.objects.create(
            name='Manage Restaurant',
            resource_type='RESTAURANT',
            action='CREATE'
        )
        
        self.role_permission = RolePermission.objects.create(
            role=self.role,
            permission=self.permission,
            access_level='FULL'
        )
        
        self.user_role = UserRole.objects.create(
            user=self.user,
            role=self.role,
            is_active=True
        )

    def test_role_assignment(self):
        """Test if user has the assigned role"""
        active_role = self.user.get_active_role()
        self.assertIsNotNone(active_role)
        self.assertEqual(active_role.role, self.role)

    def test_permission_check(self):
        """Test permission checking logic"""
        # Simulate HasModelPermission check
        has_perm = RolePermission.objects.filter(
            role=self.role,
            permission__resource_type='RESTAURANT',
            permission__action='CREATE'
        ).exists()
        
        self.assertTrue(has_perm)

    def test_unauthorized_access(self):
        """Test access without permission"""
        # Create another permission that the user doesn't have
        Permission.objects.create(
            name='Delete Restaurant',
            resource_type='RESTAURANT',
            action='DELETE'
        )
        
        has_perm = RolePermission.objects.filter(
            role=self.role,
            permission__resource_type='RESTAURANT',
            permission__action='DELETE'
        ).exists()
        
        self.assertFalse(has_perm)
