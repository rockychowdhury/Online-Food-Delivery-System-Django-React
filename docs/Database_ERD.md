# Online Food Delivery System - Database ERD

## 📊 Entity Relationship Diagram

![Online Food Delivery System ERD](https://github.com/rockychowdhury/Online-Food-Delivery-System-Django-React/blob/main/docs/assets/quickfood-erd.png?raw=true)

*Click the image to view full size. If the image doesn't load, please check the [assets folder](../docs/assets/)*

## 🎯 Database Overview

This ERD represents the complete database schema for the Online Food Delivery System built with Django and React. The system manages restaurants with multiple branches, menus, food items, user orders, payments, and ratings with a sophisticated multi-branch restaurant model.

## 📋 Core Entities

### 🏪 Restaurant Management
- **Restaurant** (`restaurant_id`): Main restaurant entity with basic information
- **Branch** (`branch_id`): Individual restaurant branches with specific locations
- **Location** (`location_id`): Geographic information with coordinates for delivery
- **Menu** (`menu_id`): Branch-specific menus that can be activated/deactivated

### 🍕 Food & Cuisine
- **FoodItem** (`food_item_id`): Individual food items with pricing and dietary info
- **Cuisines** (`cuisine_id`): Cuisine categories (Italian, Chinese, etc.)
- **Menu_FoodItem**: Junction table linking menus to food items
- **FoodItem_Cuisine**: Junction table linking food items to cuisines

### 👤 User Management
- **User** (`user_id`): Customer accounts with contact information
- **Address** (`address_id`): Customer delivery addresses
- **Rating** (`rating_id`): User reviews and ratings for food items

### 🛒 Order Management
- **OrdersGroup** (`order_group_id`): Groups orders from multiple branches into one transaction
- **Orders** (`order_id`): Individual orders from specific branches
- **OrderItem** (`order_item_id`): Specific food items within an order
- **Payments** (`payment_id`): Payment processing and status tracking

## 🔗 Key Relationships

### One-to-Many Relationships
- **Restaurant → Branch**: One restaurant can have multiple branches
- **Branch → Menu**: Each branch can have multiple menus (breakfast, lunch, dinner)
- **Branch → Orders**: Each branch processes multiple orders
- **User → Address**: Users can have multiple delivery addresses
- **User → OrdersGroup**: Users can place multiple order groups
- **User → Rating**: Users can rate multiple food items
- **OrdersGroup → Orders**: One order group can contain orders from multiple branches
- **Orders → OrderItem**: Each order contains multiple food items
- **FoodItem → Rating**: Each food item can have multiple ratings
- **FoodItem → OrderItem**: Food items can appear in multiple orders

### One-to-One Relationships
- **Location ↔ Branch**: Each branch has exactly one location
- **Payments ↔ OrdersGroup**: Each order group has one payment

### Many-to-Many Relationships
- **Menu ↔ FoodItem** (via Menu_FoodItem): Menus can contain multiple food items
- **FoodItem ↔ Cuisines** (via FoodItem_Cuisine): Food items can belong to multiple cuisines

## 🏗️ Database Schema Structure

### Primary Tables (15 entities)
```
Restaurant (4 branches) → Branch (3 menus each) → Menu → FoodItem
                                ↓
User → OrdersGroup → Orders → OrderItem → FoodItem
  ↓         ↓
Address   Payments

FoodItem ← Rating ← User
FoodItem ↔ Cuisines
```

### Junction Tables (2 entities)
- `Menu_FoodItem`: Links menus to available food items
- `FoodItem_Cuisine`: Categorizes food items by cuisine type

## 🛠️ Technical Implementation

### Data Types Used
- **INT**: Primary keys and foreign keys
- **VARCHAR**: Text fields with size limits
- **TEXT**: Large text fields (descriptions, reviews)
- **DECIMAL**: Precise monetary values and ratings
- **BOOLEAN**: Status flags (vegetarian, available, active)
- **TIMESTAMP**: Date and time tracking

### Key Features
- **Multi-branch Support**: Restaurants can have multiple locations
- **Flexible Menu System**: Each branch can have different menus
- **Grouped Orders**: Orders from multiple branches in one transaction
- **Comprehensive Rating System**: Users can rate individual food items
- **Geographic Support**: Latitude/longitude for delivery optimization

## 📁 Related Files

| File | Purpose | Location |
|------|---------|----------|
| Database Schema JSON | Complete schema definition | [`database_schema.json`](./database_schema.json) |
| Django Models | ORM model definitions | `backend/apps/*/models.py` |
| Migrations | Database migration files | `backend/apps/*/migrations/` |
| ERD Source | Editable diagram source | External tool (Eraser.io/dbdiagram.io) |

## 🔧 Tools & Technologies

- **Database**: PostgreSQL (Production) / SQLite (Development)
- **ORM**: Django ORM with model relationships
- **ERD Design**: [Eraser.io](https://app.eraser.io/) or [dbdiagram.io](https://dbdiagram.io/)
- **Backend**: Django REST Framework
- **Frontend**: React.js

## 📊 Database Statistics

- **Total Entities**: 15 tables
- **Junction Tables**: 2 (many-to-many relationships)
- **One-to-Many Relations**: 11
- **One-to-One Relations**: 2
- **Many-to-Many Relations**: 2

## 🚀 Database Setup

### Local Development
```bash
# Navigate to backend directory
cd backend/

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (if fixtures exist)
python manage.py loaddata fixtures/sample_data.json
```

### Production Deployment
```bash
# Set up PostgreSQL database
# Update DATABASE_URL in environment variables
# Run migrations
python manage.py migrate --settings=config.settings.production
```

## 💡 Design Decisions

1. **Multi-branch Architecture**: Supports restaurant chains with different locations
2. **Separated Orders and OrdersGroup**: Enables ordering from multiple branches simultaneously
3. **Flexible Menu System**: Branches can have time-specific menus (breakfast, lunch, dinner)
4. **Geographic Integration**: Location entity supports GPS coordinates for delivery routing
5. **Comprehensive Rating System**: Item-specific ratings for better food recommendations

## 🔍 Query Optimization Notes

- Index on `restaurant_id`, `branch_id`, `user_id` for faster lookups
- Composite indexes on frequently joined tables
- Consider caching for menu items and restaurant data
- Use database views for complex reporting queries

---

**Schema Version**: 1.0  
**Last Updated**: January 2025  
**Total Entities**: 15 tables, 2 junction tables  
**Project**: [Online Food Delivery System](https://github.com/rockychowdhury/Online-Food-Delivery-System-Django-React)