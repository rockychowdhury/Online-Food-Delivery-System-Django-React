
# 🍽️ QuickFood - Online Food Delivery System - Database ERD

## 📊 Entity Relationship Diagram

🔗 **[View ERD on Miro](https://miro.com/app/live-embed/uXjVLyG5xjs=/?focusWidget=3458764635736975836&embedMode=view_only_without_ui&embedId=49129292471)**

## 📋 Core Entities Overview

### 🏪 Restaurant Management
- **Restaurant**: Main entity for restaurant brands
- **Branch**: Individual physical outlets
- **Location**: Geo-tagged coordinates for each branch
- **Menu**: Branch-specific, time-based menus

### 🍕 Food & Cuisine
- **FoodItem**: Detailed food items with pricing & availability
- **Cuisines**: Cuisine classification (e.g., Italian, Indian)
- **Menu_FoodItem**: Links menu to food items
- **FoodItem_Cuisine**: Links food items to cuisines

### 👤 User & Ratings
- **User**: Customers with accounts and preferences
- **Address**: User delivery addresses
- **Rating**: User ratings of food items

### 🛒 Order System
- **OrdersGroup**: Aggregated user orders (possibly across branches)
- **Orders**: Orders per branch
- **OrderItem**: Individual items per order
- **Payments**: Associated with OrdersGroup

## 🔗 Key Relationships Summary

| Relationship                  | Type       |
|------------------------------|------------|
| Restaurant → Branch          | One-to-Many |
| Branch → Location            | One-to-One |
| Branch → Menu                | One-to-Many |
| Branch → Orders              | One-to-Many |
| Menu ↔ FoodItem              | Many-to-Many |
| FoodItem ↔ Cuisines          | Many-to-Many |
| FoodItem → Rating            | One-to-Many |
| User → Rating                | One-to-Many |
| FoodItem → OrderItem         | One-to-Many |
| Orders → OrderItem           | One-to-Many |
| OrdersGroup → Orders         | One-to-Many |
| Payments → OrdersGroup       | One-to-One |
| Address → OrdersGroup        | One-to-Many |
| User → OrdersGroup           | One-to-Many |
| User → Address               | One-to-Many |

## 🏗️ Visual Schema Structure

<div align="center">
  <img src="https://github.com/rockychowdhury/Online-Food-Delivery-System-Django-React/blob/main/docs/assets/ERD.jpg?raw=true" alt="Online Food Delivery System ERD" width="800">
</div>

## 🛠️ Schema Technologies

- **Database**: PostgreSQL (Production), SQLite (Dev)
- **ORM**: Django ORM
- **Design Tools**: dbdiagram.io, Eraser.io

## 📁 Repository References

| File                        | Purpose                          |
|-----------------------------|----------------------------------|
| `database_schema.json`      | Full schema definition           |
| `apps/*/models.py`          | Django model declarations        |
| `apps/*/migrations/`        | Database migration files         |

---

**Schema Version**: 1.0  
**Last Updated**: July 2025  
**Project**: [QuickFood - Online Food Delivery System](https://github.com/rockychowdhury/Online-Food-Delivery-System-Django-React)
