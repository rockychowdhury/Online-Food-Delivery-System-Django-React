# 🍽️ QuickFood - Online Food Delivery System

QuickFood is a comprehensive online food delivery platform that connects customers with restaurants through a multi-role system supporting restaurant owners, branch managers, delivery personnel, and customers.

## Project Structure

```
QuickFood/
├── backend/
│   ├── apps/
│   │   ├── __init__.py
│   │   ├── accounts/
│   │   ├── restaurants/
│   │   ├── orders/
│   │   ├── payments/
│   │   ├── ratings/
│   │   └── common/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   ├── production.py
│   │   │   └── testing.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/ # React client application
├── docs/
│   ├── api-documentation.md
│   ├── features-list.md
│   ├── role-based-permissions.md
│   ├── database-erd.md
│   └── readme.md
├── .env.example
└── .gitignore
```

## Features

- User authentication and authorization
- Restaurant browsing and menu management
- Order placement and tracking
- Secure payment processing
- Rating and review system
- Responsive React frontend

## Documentation

Detailed documentation is available in the [docs/](docs/) directory:

- [API Documentation](docs/api-documentation.md)
- [Features List](docs/features-list.md)
- [Role-Based Permissions](docs/role-based-permissions.md)
- [Database ERD](docs/database-erd.md)