import random
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from apps.locations.models import Country, City, Address, UserAddress
from apps.accounts.models import Role, UserRole, Permission, RolePermission
from apps.restaurants.models import Restaurant, Branch, Menu, MenuItem, Cuisine
from apps.delivery.models import DeliveryPartner, DeliveryStatus
from apps.payments.models import Payment
from apps.orders.models import OrderGroup, Order, OrderItem
from apps.ratings.models import Rating
from apps.cart.models import Cart, CartItem
from apps.common.models import Notification

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with realistic dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')
        
        try:
            with transaction.atomic():
                self.create_locations()
                users = self.create_users()
                self.create_roles_and_permissions(users)
                self.create_addresses(users)
                restaurants = self.create_restaurants(users)
                self.create_delivery_partners(users)
                self.create_orders_and_related(users, restaurants)
                self.create_carts(users, restaurants)
                self.create_notifications(users)
                
            self.stdout.write(self.style.SUCCESS('Successfully populated database!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error populating database: {str(e)}'))
            raise e

    def create_locations(self):
        self.stdout.write('Creating locations...')
        countries = [
            ('United States', 'US', 'USD', 'America/New_York'),
            ('United Kingdom', 'UK', 'GBP', 'Europe/London'),
            ('Canada', 'CA', 'CAD', 'America/Toronto'),
        ]
        
        created_countries = []
        for name, code, currency, tz in countries:
            c, _ = Country.objects.get_or_create(
                code=code,
                defaults={'name': name, 'currency': currency, 'timezone': tz}
            )
            created_countries.append(c)

        cities_data = {
            'US': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            'UK': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow'],
            'CA': ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Ottawa']
        }

        for country in created_countries:
            for city_name in cities_data.get(country.code, []):
                City.objects.get_or_create(country=country, name=city_name)

    def create_users(self):
        self.stdout.write('Creating users...')
        users = []
        names = [
            ('James', 'Smith'), ('Mary', 'Johnson'), ('Robert', 'Williams'), ('Patricia', 'Brown'),
            ('John', 'Jones'), ('Jennifer', 'Garcia'), ('Michael', 'Miller'), ('Linda', 'Davis'),
            ('David', 'Rodriguez'), ('Elizabeth', 'Martinez'), ('William', 'Hernandez'), ('Barbara', 'Lopez'),
            ('Richard', 'Gonzalez'), ('Susan', 'Wilson'), ('Joseph', 'Anderson'), ('Jessica', 'Thomas'),
            ('Thomas', 'Taylor'), ('Sarah', 'Moore'), ('Charles', 'Jackson'), ('Karen', 'Martin')
        ]

        for i, (first, last) in enumerate(names):
            email = f"{first.lower()}.{last.lower()}{i}@example.com"
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'first_name': first,
                    'last_name': last,
                    'phone': f"+1555{str(i).zfill(7)}",
                    'is_active': True,
                    'is_email_verified': True,
                    'is_phone_verified': True if i % 2 == 0 else False
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        return users

    def create_roles_and_permissions(self, users):
        self.stdout.write('Creating roles and permissions...')
        roles_data = [
            ('CUSTOMER', 'Customer', 'PLATFORM'),
            ('RESTAURANT_ADMIN', 'Restaurant Admin', 'RESTAURANT'),
            ('DELIVERY_PARTNER', 'Delivery Partner', 'PLATFORM'),
            ('SUPER_ADMIN', 'Super Admin', 'SYSTEM'),
        ]
        
        created_roles = {}
        for name, label, rtype in roles_data:
            role, _ = Role.objects.get_or_create(
                name=name,
                defaults={'role_type': rtype, 'description': f'{label} role'}
            )
            created_roles[name] = role

        # Assign roles to users
        # First user is Super Admin
        UserRole.objects.get_or_create(user=users[0], role=created_roles['SUPER_ADMIN'])
        
        # Next 5 are Restaurant Admins
        for user in users[1:6]:
            UserRole.objects.get_or_create(user=user, role=created_roles['RESTAURANT_ADMIN'])
            
        # Next 5 are Delivery Partners
        for user in users[6:11]:
            UserRole.objects.get_or_create(user=user, role=created_roles['DELIVERY_PARTNER'])
            
        # Rest are Customers
        for user in users[11:]:
            UserRole.objects.get_or_create(user=user, role=created_roles['CUSTOMER'])

    def create_addresses(self, users):
        self.stdout.write('Creating addresses...')
        cities = list(City.objects.all())
        streets = ['Main St', 'Broadway', 'Park Ave', 'Oak Ln', 'Maple Dr', 'Cedar Ct', 'Elm St', 'Washington Blvd']
        
        for user in users:
            for i in range(random.randint(1, 2)):
                city = random.choice(cities)
                address, _ = Address.objects.get_or_create(
                    street_address=f"{random.randint(100, 9999)} {random.choice(streets)}",
                    city=city,
                    defaults={
                        'state': 'State',
                        'postal_code': f"{random.randint(10000, 99999)}",
                        'latitude': random.uniform(25.0, 48.0),
                        'longitude': random.uniform(-120.0, -70.0)
                    }
                )
                
                UserAddress.objects.get_or_create(
                    user=user,
                    address=address,
                    defaults={
                        'address_type': random.choice(['home', 'work', 'other']),
                        'is_default': i == 0
                    }
                )

    def create_restaurants(self, users):
        self.stdout.write('Creating restaurants...')
        cuisines_list = ['Italian', 'Chinese', 'Indian', 'Mexican', 'Japanese', 'American', 'Thai', 'French']
        cuisines = []
        for c in cuisines_list:
            cuisine, _ = Cuisine.objects.get_or_create(name=c)
            cuisines.append(cuisine)

        restaurant_names = [
            'The Golden Spoon', 'Spice Garden', 'Pasta Palace', 'Burger Joint', 'Sushi World',
            'Taco Fiesta', 'Curry House', 'Pizza Planet', 'Wok & Roll', 'The French Connection'
        ]

        restaurant_admins = users[1:6] # Reusing the admins identified earlier
        created_restaurants = []

        for i, name in enumerate(restaurant_names):
            owner = restaurant_admins[i % len(restaurant_admins)]
            restaurant, _ = Restaurant.objects.get_or_create(
                name=name,
                defaults={
                    'owner': owner,
                    'phone': f"+1555999{str(i).zfill(4)}",
                    'email': f"contact@{name.lower().replace(' ', '')}.com",
                    'description': f"Best {name} in town!"
                }
            )
            created_restaurants.append(restaurant)

            # Create Branch
            cities = list(City.objects.all())
            city = random.choice(cities)
            address, _ = Address.objects.get_or_create(
                street_address=f"{random.randint(100, 9999)} {name} Blvd",
                city=city,
                defaults={
                    'state': 'State',
                    'postal_code': '12345',
                    'latitude': random.uniform(25.0, 48.0),
                    'longitude': random.uniform(-120.0, -70.0)
                }
            )
            
            branch, _ = Branch.objects.get_or_create(
                restaurant=restaurant,
                name="Main Branch",
                defaults={
                    'address': address,
                    'phone': restaurant.phone,
                    'latitude': address.latitude,
                    'longitude': address.longitude
                }
            )

            # Create Menu
            menu, _ = Menu.objects.get_or_create(
                branch=branch,
                name="Standard Menu",
                defaults={'description': 'All day menu'}
            )

            # Create Menu Items
            food_items = {
                'Italian': [('Spaghetti Carbonara', 15.99), ('Margherita Pizza', 12.99), ('Tiramisu', 8.99)],
                'American': [('Cheeseburger', 10.99), ('Fries', 4.99), ('Milkshake', 5.99)],
                'Japanese': [('Sushi Roll', 8.99), ('Ramen', 13.99), ('Tempura', 11.99)],
                'Mexican': [('Tacos', 3.99), ('Burrito', 9.99), ('Guacamole', 5.99)],
                'Indian': [('Butter Chicken', 16.99), ('Naan', 2.99), ('Samosa', 4.99)]
            }
            
            # Assign a random cuisine to the restaurant for menu generation purposes
            rest_cuisine_name = random.choice(list(food_items.keys()))
            rest_cuisine = Cuisine.objects.get(name=rest_cuisine_name) # Ensure we get the object
            
            for item_name, price in food_items[rest_cuisine_name]:
                MenuItem.objects.get_or_create(
                    menu=menu,
                    name=item_name,
                    defaults={
                        'description': f"Delicious {item_name}",
                        'price': price,
                        'cuisine': rest_cuisine,
                        'is_available': True
                    }
                )
        
        return created_restaurants

    def create_delivery_partners(self, users):
        self.stdout.write('Creating delivery partners...')
        partners = users[6:11]
        for user in partners:
            DeliveryPartner.objects.get_or_create(
                user=user,
                defaults={
                    'vehicle_type': random.choice(['Bike', 'Scooter', 'Car']),
                    'average_rating': random.uniform(3.5, 5.0),
                    'is_active': True
                }
            )
        
        statuses = ['PENDING', 'CONFIRMED', 'PREPARING', 'READY_FOR_PICKUP', 'OUT_FOR_DELIVERY', 'DELIVERED', 'CANCELLED']
        for s in statuses:
            DeliveryStatus.objects.get_or_create(status=s)

    def create_orders_and_related(self, users, restaurants):
        self.stdout.write('Creating orders...')
        customers = users[11:] # Use users who are primarily customers
        delivery_partners = DeliveryPartner.objects.all()
        delivery_statuses = DeliveryStatus.objects.all()

        for _ in range(20): # Create 20 orders
            customer = random.choice(customers)
            restaurant = random.choice(restaurants)
            branch = Branch.objects.filter(restaurant=restaurant).first()
            menu = Menu.objects.filter(branch=branch).first()
            if not menu: continue
            
            menu_items = list(MenuItem.objects.filter(menu=menu))
            if not menu_items: continue
            
            # Create Payment
            total_amount = 0
            selected_items = random.sample(menu_items, k=random.randint(1, 3))
            
            # Calculate total first
            for item in selected_items:
                total_amount += item.price * random.randint(1, 2)

            payment = Payment.objects.create(
                user=customer,
                amount=total_amount,
                method=random.choice(['CREDIT_CARD', 'PAYPAL', 'CASH']),
                transaction_id=f"TXN-{random.randint(100000, 999999)}",
                status='COMPLETED',
                paid_at=timezone.now()
            )

            # Create OrderGroup
            order_group = OrderGroup.objects.create(
                customer=customer,
                status='COMPLETED',
                total_price=total_amount,
                payment=payment
            )

            # Create Order
            status = random.choice(delivery_statuses)
            partner = random.choice(delivery_partners) if status.status in ['OUT_FOR_DELIVERY', 'DELIVERED'] else None
            
            order = Order.objects.create(
                order_group=order_group,
                restaurant=restaurant,
                delivery_status=status,
                total_price=total_amount,
                delivery_partner=partner
            )

            # Create OrderItems
            for item in selected_items:
                qty = random.randint(1, 2)
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=qty,
                    price=item.price,
                    special_instructions="No onions" if random.choice([True, False]) else ""
                )

            # Create Rating (if delivered)
            if status.status == 'DELIVERED':
                Rating.objects.create(
                    user=customer,
                    order=order,
                    delivery_partner=partner,
                    score=random.randint(1, 5),
                    comment="Great food!" if random.choice([True, False]) else ""
                )

    def create_carts(self, users, restaurants):
        self.stdout.write('Creating carts...')
        customers = users[11:]
        for customer in customers:
            cart, _ = Cart.objects.get_or_create(user=customer)
            
            # Add some items
            restaurant = random.choice(restaurants)
            branch = Branch.objects.filter(restaurant=restaurant).first()
            if branch:
                menu = Menu.objects.filter(branch=branch).first()
                if menu:
                    items = list(MenuItem.objects.filter(menu=menu))
                    if items:
                        for _ in range(random.randint(1, 3)):
                            item = random.choice(items)
                            CartItem.objects.get_or_create(
                                cart=cart,
                                menu_item=item,
                                defaults={'quantity': random.randint(1, 3)}
                            )

    def create_notifications(self, users):
        self.stdout.write('Creating notifications...')
        for user in users:
            for _ in range(random.randint(1, 5)):
                Notification.objects.create(
                    user=user,
                    message=f"Your order #{random.randint(1000, 9999)} has been updated.",
                    read=random.choice([True, False])
                )
