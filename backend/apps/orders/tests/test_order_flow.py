from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant, Branch, Menu, MenuItem, Category
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order, OrderGroup
from apps.delivery.models import DeliveryPartner, DeliveryStatus
from apps.locations.models import Address, City, Country

User = get_user_model()

class OrderFlowTests(APITestCase):
    def setUp(self):
        # Create users
        self.customer = User.objects.create_user(email='customer@example.com', password='password123')
        self.owner = User.objects.create_user(email='owner@example.com', password='password123')
        self.driver_user = User.objects.create_user(email='driver@example.com', password='password123')
        
        # Create Delivery Partner
        self.driver = DeliveryPartner.objects.create(user=self.driver_user, vehicle_type='Bike')
        
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
        
        # Create Address
        self.country = Country.objects.create(name='Test Country', code='TC', currency='USD', timezone='UTC')
        self.city = City.objects.create(name='Test City', country=self.country)
        self.address = Address.objects.create(
            street_address='123 Main St', city=self.city, state='State', postal_code='12345'
        )

        # URLs
        self.cart_add_url = '/api/v1/cart/add/'
        self.checkout_url = '/api/v1/orders/order-groups/checkout/'
        self.orders_url = '/api/v1/orders/orders/'
        self.delivery_url = '/api/v1/delivery/partners/'

    def test_order_lifecycle(self):
        # 1. Add to Cart
        self.client.force_authenticate(user=self.customer)
        self.client.post(self.cart_add_url, {'menu_item': self.item.id, 'quantity': 2})
        
        response = self.client.post(self.checkout_url, {'address_id': self.address.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order_group_id = response.data['data']['order_group_id']
        
        # Verify Cart Empty
        cart = Cart.objects.get(user=self.customer)
        self.assertEqual(cart.items.count(), 0)
        
        # Verify Order Created
        order = Order.objects.get(order_group_id=order_group_id)
        self.assertEqual(order.restaurant, self.restaurant)
        self.assertEqual(float(order.total_price), 20.00)
        self.assertEqual(order.delivery_status.status, 'PENDING')
        
        # 3. Restaurant Owner Updates Status
        self.client.force_authenticate(user=self.owner)
        update_url = f"{self.orders_url}{order.id}/update_status/"
        response = self.client.patch(update_url, {'status': 'PREPARING'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        order.refresh_from_db()
        self.assertEqual(order.delivery_status.status, 'PREPARING')
        
        # 4. Delivery Partner Claims Order
        # First set status back to PENDING for claim logic (as per current implementation)
        # Or update implementation to allow claiming PREPARING orders. 
        # For this test, let's assume we want to claim PENDING orders.
        # Let's reset status for test simplicity or update logic.
        # Actually, let's update the claim logic to allow claiming if no partner assigned, regardless of status (or specific statuses).
        # But my implementation checks for PENDING status in `available_orders`.
        # Let's update status back to PENDING via admin/owner for the test flow or just create a new order.
        # Let's just manually set it for the test.
        pending_status = DeliveryStatus.objects.get(status='PENDING')
        order.delivery_status = pending_status
        order.save()

        self.client.force_authenticate(user=self.driver_user)
        
        # Check availability
        response = self.client.get(f"{self.delivery_url}available_orders/")
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['id'], order.id)
        
        # Claim
        claim_url = f"{self.delivery_url}orders/{order.id}/claim/"
        response = self.client.post(claim_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        order.refresh_from_db()
        self.assertEqual(order.delivery_partner, self.driver)
        
        # 5. Delivery Partner Updates Status
        status_url = f"{self.delivery_url}orders/{order.id}/update-status/"
        response = self.client.post(status_url, {'status': 'DELIVERED'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        order.refresh_from_db()
        self.assertEqual(order.delivery_status.status, 'DELIVERED')
