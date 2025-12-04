from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant, Branch, Menu, MenuItem, Category
from apps.cart.models import Cart, CartItem

User = get_user_model()

class CartFlowTests(APITestCase):
    def setUp(self):
        # Create users
        self.customer = User.objects.create_user(email='customer@example.com', password='password123')
        self.owner = User.objects.create_user(email='owner@example.com', password='password123')
        
        # Create Restaurant & Menu Item
        self.restaurant = Restaurant.objects.create(
            name='Pizza Place', owner=self.owner, 
            phone='123', email='pizza@example.com', 
            is_approved=True, is_active=True
        )
        self.branch = Branch.objects.create(
            restaurant=self.restaurant, name='Main Branch', phone='123'
        )
        self.menu = Menu.objects.create(branch=self.branch, name='Main Menu')
        self.category = Category.objects.create(name='Pizza')
        self.item = MenuItem.objects.create(
            menu=self.menu, category=self.category, name='Cheese Pizza', 
            price='10.00', is_available=True
        )
        
        self.cart_url = '/api/v1/cart/'
        self.add_url = '/api/v1/cart/add/'

    def test_cart_lifecycle(self):
        self.client.force_authenticate(user=self.customer)
        
        # 1. Get empty cart (should create one)
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['items']), 0)
        self.assertEqual(float(response.data['data']['total_price']), 0.00)
        
        # 2. Add item to cart
        data = {'menu_item': self.item.id, 'quantity': 2}
        response = self.client.post(self.add_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify cart state
        response = self.client.get(self.cart_url)
        self.assertEqual(len(response.data['data']['items']), 1)
        self.assertEqual(float(response.data['data']['total_price']), 20.00) # 10.00 * 2
        cart_item_id = response.data['data']['items'][0]['id']
        
        # 3. Update quantity
        update_url = f"{self.cart_url}items/{cart_item_id}/"
        response = self.client.patch(update_url, {'quantity': 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify update
        response = self.client.get(self.cart_url)
        self.assertEqual(float(response.data['data']['total_price']), 30.00)
        
        # 4. Remove item
        response = self.client.delete(update_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify empty
        response = self.client.get(self.cart_url)
        self.assertEqual(len(response.data['data']['items']), 0)
        self.assertEqual(float(response.data['data']['total_price']), 0.00)
