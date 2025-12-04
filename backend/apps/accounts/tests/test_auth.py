from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import Role, UserRole

User = get_user_model()

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('token_pair')
        self.logout_url = reverse('remove_cookies')
        self.refresh_url = reverse('refresh_token')
        self.password_reset_request_url = reverse('password_reset_request')
        self.password_reset_confirm_url = reverse('password_reset_confirm')
        
        self.user_data = {
            'email': 'test@example.com',
            'password': 'StrongPassword123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        # Create a role for testing
        self.role = Role.objects.create(
            name=Role.RoleName.CUSTOMER,
            role_type=Role.RoleType.PLATFORM
        )

    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_user_login(self):
        """Test user login"""
        # Create user first
        user = User.objects.create_user(**self.user_data)
        
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)

    def test_token_refresh(self):
        """Test token refresh"""
        user = User.objects.create_user(**self.user_data)
        
        # Login to get refresh token
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(self.login_url, login_data)
        refresh_token = login_response.cookies['refresh_token'].value
        
        # Use refresh token to get new access token
        self.client.cookies['refresh_token'] = refresh_token
        response = self.client.post(self.refresh_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.cookies)

    def test_logout(self):
        """Test logout"""
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if cookies are cleared (value is empty string)
        self.assertEqual(response.cookies['access_token'].value, '')
        self.assertEqual(response.cookies['refresh_token'].value, '')

    def test_password_reset_request(self):
        """Test password reset request"""
        data = {'email': self.user_data['email']}
        response = self.client.post(self.password_reset_request_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_confirm(self):
        """Test password reset confirm"""
        data = {
            'token': 'dummy-token',
            'uidb64': 'dummy-uid',
            'new_password': 'NewStrongPassword123!'
        }
        response = self.client.post(self.password_reset_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
