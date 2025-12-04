from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant, Branch, Menu, MenuItem, Category

User = get_user_model()

class RestaurantFlowTests(APITestCase):
    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(email='owner@example.com', password='password123', first_name='Owner')
        self.admin = User.objects.create_user(email='admin@example.com', password='password123', is_staff=True)
        self.customer = User.objects.create_user(email='customer@example.com', password='password123')
        
        # URLs
        self.restaurants_url = '/api/v1/restaurants/restaurants/'
        self.branches_url = '/api/v1/restaurants/branches/'
        self.menus_url = '/api/v1/restaurants/menus/'
        self.menu_items_url = '/api/v1/restaurants/menu-items/'

    def test_restaurant_creation_and_approval(self):
        # 1. Owner creates restaurant
        self.client.force_authenticate(user=self.owner)
        data = {
            'name': 'Test Restaurant',
            'phone': '1234567890',
            'email': 'test@example.com',
            'description': 'Test Description'
        }
        response = self.client.post(self.restaurants_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        restaurant_id = response.data['id']
        
        # Verify status is pending (not approved)
        restaurant = Restaurant.objects.get(id=restaurant_id)
        self.assertFalse(restaurant.is_approved)
        
        # 2. Verify public cannot see it
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(self.restaurants_url)
        if response.data['count'] != 0:
            print(f"Unexpected Restaurants: {response.data}")
        self.assertEqual(response.data['count'], 0)
        
        # 3. Admin approves restaurant
        self.client.force_authenticate(user=self.admin)
        approve_url = f"{self.restaurants_url}{restaurant_id}/approve/"
        response = self.client.post(approve_url, {'is_approved': True, 'is_active': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Verify public can see it now
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(self.restaurants_url)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Restaurant')

    def test_menu_management(self):
        # Setup approved restaurant
        restaurant = Restaurant.objects.create(
            name='Approved Restaurant', owner=self.owner, 
            phone='123', email='a@a.com', is_approved=True, is_active=True
        )
        branch = Branch.objects.create(
            restaurant=restaurant, name='Main Branch', phone='123'
        )
        
        # 1. Create Category
        self.client.force_authenticate(user=self.owner)
        cat_url = '/api/v1/restaurants/categories/'
        response = self.client.post(cat_url, {'name': 'Pizza'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = response.data['id']
        
        # 2. Create Menu
        response = self.client.post(self.menus_url, {
            'branch': branch.id,
            'name': 'Lunch Menu'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        menu_id = response.data['id']
        
        # 3. Add Menu Item with details
        item_data = {
            'menu': menu_id,
            'category_id': category_id,
            'cuisine_id': None,
            'name': 'Veggie Pizza',
            'price': '15.00',
            'ingredients': 'Cheese, Tomato, Basil',
            'allergens': 'Dairy, Gluten',
            'is_vegetarian': True
        }
        response = self.client.post(self.menu_items_url, item_data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Menu Item Creation Error: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify details
        item = MenuItem.objects.get(id=response.data['id'])
        self.assertTrue(item.is_vegetarian)
        self.assertEqual(item.ingredients, 'Cheese, Tomato, Basil')
