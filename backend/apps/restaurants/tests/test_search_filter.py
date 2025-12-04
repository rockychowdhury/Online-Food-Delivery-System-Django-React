from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant, Branch, Menu, MenuItem, Category, Cuisine

User = get_user_model()

class SearchFilterTests(APITestCase):
    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(email='owner@example.com', password='password123')
        self.customer = User.objects.create_user(email='customer@example.com', password='password123')
        
        # Create Restaurant
        self.restaurant = Restaurant.objects.create(
            name='Pizza Palace', owner=self.owner, 
            phone='123', email='pizza@example.com', 
            is_approved=True, is_active=True,
            description='Best Pizza in town'
        )
        self.branch = Branch.objects.create(
            restaurant=self.restaurant, name='Main Branch', phone='123'
        )
        self.menu = Menu.objects.create(branch=self.branch, name='Main Menu')
        self.category = Category.objects.create(name='Pizza')
        
        # Create Items
        self.item1 = MenuItem.objects.create(
            menu=self.menu, category=self.category, name='Veggie Pizza', 
            price='10.00', is_vegetarian=True, is_available=True
        )
        self.item2 = MenuItem.objects.create(
            menu=self.menu, category=self.category, name='Meat Lover', 
            price='15.00', is_vegetarian=False, is_available=True
        )

        self.restaurants_url = '/api/v1/restaurants/restaurants/'
        self.menu_items_url = '/api/v1/restaurants/menu-items/'

    def test_search_restaurant(self):
        self.client.force_authenticate(user=self.customer)
        
        # Search match
        response = self.client.get(f"{self.restaurants_url}?search=Pizza")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Pizza Palace')
        
        # Search no match
        response = self.client.get(f"{self.restaurants_url}?search=Burger")
        self.assertEqual(response.data['count'], 0)

    def test_filter_menu_items(self):
        self.client.force_authenticate(user=self.customer)
        
        # Filter vegetarian
        response = self.client.get(f"{self.menu_items_url}?is_vegetarian=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Veggie Pizza')
        
        # Filter non-vegetarian (implicit by exclusion or explicit False)
        response = self.client.get(f"{self.menu_items_url}?is_vegetarian=False")
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Meat Lover')

    def test_ordering_menu_items(self):
        self.client.force_authenticate(user=self.customer)
        
        # Order by price ascending
        response = self.client.get(f"{self.menu_items_url}?ordering=price")
        self.assertEqual(response.data['results'][0]['name'], 'Veggie Pizza') # 10.00
        self.assertEqual(response.data['results'][1]['name'], 'Meat Lover')   # 15.00
        
        # Order by price descending
        response = self.client.get(f"{self.menu_items_url}?ordering=-price")
        self.assertEqual(response.data['results'][0]['name'], 'Meat Lover')
        self.assertEqual(response.data['results'][1]['name'], 'Veggie Pizza')
